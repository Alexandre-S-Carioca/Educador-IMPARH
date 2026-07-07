import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import '../application/course_repository.dart';
import '../domain/course_models.dart';
import '../../gamification/application/progress_repository.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  String? _selectedCourseId;

  @override
  Widget build(BuildContext context) {
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
      ),
      body: coursesAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Erro ao carregar cursos: $err')),
        data: (courses) {
          if (courses.isEmpty) {
            return const Center(child: Text('Nenhum curso disponível.'));
          }

          _selectedCourseId ??= courses.first.id;

          final selectedCourse = courses.firstWhere(
            (c) => c.id == _selectedCourseId,
            orElse: () => courses.first,
          );

          final modulesAsync = ref.watch(modulesProvider(selectedCourse.id));

          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                height: 54,
                color: Colors.white,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  itemCount: courses.length,
                  itemBuilder: (context, index) {
                    final course = courses[index];
                    final isSelected = course.id == _selectedCourseId;
                    
                    return Padding(
                      padding: const EdgeInsets.only(right: 8.0),
                      child: FilterChip(
                        selected: isSelected,
                        showCheckmark: false,
                        label: Text(
                          course.name.replaceAll('Português - ', ''),
                          style: GoogleFonts.inter(
                            fontWeight: FontWeight.bold,
                            fontSize: 12,
                            color: isSelected ? Colors.white : Colors.grey.shade700,
                          ),
                        ),
                        selectedColor: Colors.blueAccent.shade700,
                        onSelected: (selected) {
                          if (selected) {
                            setState(() {
                              _selectedCourseId = course.id;
                            });
                          }
                        },
                      ),
                    );
                  },
                ),
              ),
              const Divider(height: 1),
              Expanded(
                child: modulesAsync.when(
                  loading: () => const Center(child: CircularProgressIndicator()),
                  error: (err, stack) => Center(child: Text('Erro ao carregar módulos: $err')),
                  data: (modules) {
                    if (modules.isEmpty) {
                      return Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.menu_book_outlined, size: 48, color: Colors.grey.shade400),
                            const SizedBox(height: 12),
                            Text(
                              'Nenhum módulo nesta trilha ainda.',
                              style: GoogleFonts.inter(color: Colors.grey.shade500, fontSize: 14),
                            ),
                          ],
                        ),
                      );
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
                ),
              ),
            ],
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
