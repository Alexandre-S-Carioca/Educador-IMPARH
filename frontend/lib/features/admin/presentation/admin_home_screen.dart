import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import '../../course/application/course_repository.dart';
import '../../course/domain/course_models.dart';

class AdminHomeScreen extends ConsumerWidget {
  const AdminHomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final coursesAsync = ref.watch(coursesProvider);

    return Scaffold(
      backgroundColor: Colors.blueGrey.shade50,
      appBar: AppBar(
        title: Text('Painel do Professor', style: GoogleFonts.inter(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.blueGrey.shade900,
        foregroundColor: Colors.white,
      ),
      body: coursesAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Erro: $err')),
        data: (courses) {
          if (courses.isEmpty) return const Center(child: Text('Nenhum curso.'));
          
          final courseId = courses.first.id;
          final modulesAsync = ref.watch(modulesProvider(courseId));

          return modulesAsync.when(
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (err, stack) => Center(child: Text('Erro: $err')),
            data: (modules) {
              return ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: modules.length,
                itemBuilder: (context, mIndex) {
                  final module = modules[mIndex];
                  return Card(
                    elevation: 1,
                    margin: const EdgeInsets.only(bottom: 16),
                    child: ExpansionTile(
                      title: Text(module.title, style: GoogleFonts.inter(fontWeight: FontWeight.bold)),
                      children: module.units.map((unit) {
                        return Column(
                          children: [
                            ListTile(
                              title: Text(unit.title, style: GoogleFonts.inter(fontWeight: FontWeight.bold, color: Colors.blueGrey)),
                              trailing: ElevatedButton.icon(
                                style: ElevatedButton.styleFrom(backgroundColor: Colors.blueGrey.shade800, foregroundColor: Colors.white),
                                onPressed: () {
                                  context.push('/admin/unit/${unit.id}/create-topic');
                                },
                                icon: const Icon(Icons.add, size: 18),
                                label: const Text('Tópico'),
                              ),
                            ),
                            ...unit.topics.map((topic) => ListTile(
                                  contentPadding: const EdgeInsets.only(left: 32, right: 16),
                                  title: Text(topic.title),
                                  trailing: IconButton(
                                    icon: const Icon(Icons.add_task, color: Colors.green),
                                    onPressed: () {
                                      context.push('/admin/topic/${topic.id}/create-question');
                                    },
                                    tooltip: 'Adicionar Questão',
                                  ),
                                ))
                          ],
                        );
                      }).toList(),
                    ),
                  );
                },
              );
            },
          );
        },
      ),
    );
  }
}
