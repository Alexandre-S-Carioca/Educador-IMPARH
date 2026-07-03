import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import 'package:go_router/go_router.dart';
import '../application/course_repository.dart';
import '../domain/course_models.dart';
import '../../gamification/application/progress_repository.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final coursesAsync = ref.watch(coursesProvider);
    final progressAsync = ref.watch(progressSummaryProvider);

    return Scaffold(
      backgroundColor: Colors.grey.shade50,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.blueAccent.shade700,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Trilhas de Estudo',
              style: GoogleFonts.inter(fontWeight: FontWeight.bold, color: Colors.white),
            ),
            progressAsync.when(
              data: (progress) => Text(
                'Nível ${progress.level} • ${progress.totalXp} XP',
                style: GoogleFonts.inter(fontSize: 12, color: Colors.blue.shade100, fontWeight: FontWeight.w600),
              ),
              loading: () => const SizedBox(),
              error: (err, stack) => const SizedBox(),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.account_circle, color: Colors.white),
            onPressed: () {},
          )
        ],
      ),
      body: coursesAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Erro ao carregar cursos: $err')),
        data: (courses) {
          if (courses.isEmpty) {
            return const Center(child: Text('Nenhum curso disponível.'));
          }
          final courseId = courses.first.id;
          final modulesAsync = ref.watch(modulesProvider(courseId));

          return modulesAsync.when(
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (err, stack) => Center(child: Text('Erro ao carregar módulos: $err')),
            data: (modules) {
              if (modules.isEmpty) {
                return const Center(child: Text('Nenhum módulo encontrado.'));
              }
              return ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: modules.length,
                itemBuilder: (context, index) {
                  final module = modules[index];
                  return _buildModuleCard(context, module);
                },
              );
            },
          );
        },
      ),
    );
  }

  Widget _buildModuleCard(BuildContext context, Module module) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ExpansionTile(
        tilePadding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
        leading: Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: Colors.blueAccent.shade100.withOpacity(0.3),
            shape: BoxShape.circle,
          ),
          child: Icon(Icons.menu_book, color: Colors.blueAccent.shade700),
        ),
        title: Text(
          module.title,
          style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 18),
        ),
        children: module.units.map((unit) {
          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.only(left: 72, top: 8, bottom: 4),
                child: Text(
                  unit.title,
                  style: GoogleFonts.inter(fontWeight: FontWeight.w600, color: Colors.grey.shade800),
                ),
              ),
              ...unit.topics.map((topic) => ListTile(
                    contentPadding: const EdgeInsets.only(left: 72, right: 24),
                    title: Text(topic.title, style: GoogleFonts.inter(fontSize: 14)),
                    trailing: const Icon(Icons.play_circle_fill, color: Colors.blueAccent),
                    onTap: () {
                      context.push('/topic/${topic.id}');
                    },
                  ))
            ],
          );
        }).toList(),
      ),
    );
  }
}
