import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import '../application/course_repository.dart';
import '../../gamification/application/activity_log_repository.dart';

class TopicScreen extends ConsumerWidget {
  final String topicId;

  const TopicScreen({super.key, required this.topicId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.listen<AsyncValue>(topicDetailProvider(topicId), (previous, next) {
      next.whenOrNull(
        data: (topic) {
          ref.read(activityLogRepositoryProvider).recordActivityLog(
            'VIEW_TOPIC',
            'Visualizou o tópico "${topic.title}"',
          );
        },
      );
    });

    final topicAsync = ref.watch(topicDetailProvider(topicId));

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.blueAccent.shade700,
        foregroundColor: Colors.white,
        title: Text(
          'Teoria',
          style: GoogleFonts.inter(fontWeight: FontWeight.bold),
        ),
      ),
      body: topicAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Erro: $err')),
        data: (topic) {
          return Column(
            children: [
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        topic.title,
                        style: GoogleFonts.inter(
                          fontSize: 28,
                          fontWeight: FontWeight.bold,
                          color: Colors.blueAccent.shade700,
                        ),
                      ),
                      const SizedBox(height: 16),
                      if (topic.introduction != null) ...[
                        Text(
                          topic.introduction!,
                          style: GoogleFonts.inter(
                            fontSize: 18,
                            color: Colors.grey.shade700,
                            fontStyle: FontStyle.italic,
                          ),
                        ),
                        const SizedBox(height: 24),
                      ],
                      MarkdownBody(
                        data: topic.theoryMarkdown ?? '*Nenhuma teoria adicionada ainda.*',
                        styleSheet: MarkdownStyleSheet(
                          p: GoogleFonts.inter(fontSize: 16, height: 1.6, color: Colors.grey.shade800),
                          h1: GoogleFonts.inter(fontSize: 24, fontWeight: FontWeight.bold),
                          h2: GoogleFonts.inter(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.blueAccent),
                          listBullet: TextStyle(color: Colors.blueAccent.shade700),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              if (topic.questions.isNotEmpty)
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.grey.shade50,
                    border: Border(top: BorderSide(color: Colors.grey.shade200)),
                  ),
                  child: Column(
                    children: [
                      SizedBox(
                        height: 50,
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.blueAccent.shade700,
                            foregroundColor: Colors.white,
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          icon: const Icon(Icons.play_arrow),
                          label: Text('PRACTICE (${topic.questions.length} Questões)', style: GoogleFonts.inter(fontWeight: FontWeight.bold)),
                          onPressed: () {
                            context.push('/topic/${topic.id}/quiz');
                          },
                        ),
                      ),
                      const SizedBox(height: 12),
                      SizedBox(
                        height: 50,
                        width: double.infinity,
                        child: OutlinedButton.icon(
                          style: OutlinedButton.styleFrom(
                            foregroundColor: Colors.deepPurple,
                            side: const BorderSide(color: Colors.deepPurple, width: 2),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          icon: const Icon(Icons.style),
                          label: Text('Revisar Flashcards 🃏', style: GoogleFonts.inter(fontWeight: FontWeight.bold)),
                          onPressed: () {
                            context.push('/topic/${topic.id}/flashcards');
                          },
                        ),
                      ),
                    ],
                  ),
                )
            ],
          );
        },
      ),
    );
  }
}
