import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import '../application/course_repository.dart';
import '../application/classroom_repository.dart';
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
                      
                      // Seção de Pronúncia/Fonética (Áudio com IPA)
                      _buildAudioSection(context, ref, topic.id),
                      
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
                      
                      const SizedBox(height: 32),
                      const Divider(),
                      const SizedBox(height: 20),
                      // Seção "Videoaulas Recomendadas" (YouTube)
                      _buildYouTubeSection(context, ref, topic.title),
                      
                      const SizedBox(height: 20),
                      // Seção "Saiba Mais com a Wikipedia"
                      _buildWikiSection(context, ref, topic.title),
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

  Widget _buildAudioSection(BuildContext context, WidgetRef ref, String topicId) {
    final audioAsync = ref.watch(topicAudioProvider(topicId));

    return audioAsync.when(
      loading: () => const SizedBox(),
      error: (err, stack) => const SizedBox(),
      data: (audios) {
        if (audios.isEmpty) return const SizedBox();

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 12),
            Text(
              'Pronúncia & Fonética (IPA):',
              style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 14, color: Colors.blueAccent.shade700),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 12,
              runSpacing: 8,
              children: audios.map((audio) {
                return Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  decoration: BoxDecoration(
                    color: Colors.blue.shade50.withOpacity(0.3),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: Colors.blue.shade100.withOpacity(0.5)),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      GestureDetector(
                        onTap: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Row(
                                children: [
                                  const Icon(Icons.volume_up, color: Colors.white),
                                  const SizedBox(width: 8),
                                  Text('Reproduzindo áudio de "${audio.wordOrPhrase}"...'),
                                ],
                              ),
                              backgroundColor: Colors.blueAccent.shade700,
                              duration: const Duration(seconds: 2),
                            ),
                          );
                        },
                        child: Icon(Icons.volume_up, size: 18, color: Colors.blueAccent.shade700),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        audio.wordOrPhrase,
                        style: GoogleFonts.inter(fontWeight: FontWeight.w600, fontSize: 13),
                      ),
                      if (audio.ipaPhonetic != null) ...[
                        const SizedBox(width: 6),
                        Text(
                          audio.ipaPhonetic!,
                          style: GoogleFonts.inter(
                            fontSize: 12,
                            color: Colors.indigo.shade600,
                            fontStyle: FontStyle.italic,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ],
                    ],
                  ),
                );
              }).toList(),
            ),
            const SizedBox(height: 16),
            const Divider(),
          ],
        );
      },
    );
  }

  Widget _buildWikiSection(BuildContext context, WidgetRef ref, String topicTitle) {
    final wikiAsync = ref.watch(wikiSummaryProvider(topicTitle));

    return wikiAsync.when(
      loading: () => const Padding(
        padding: EdgeInsets.symmetric(vertical: 16.0),
        child: Center(
          child: SizedBox(
            height: 20,
            width: 20,
            child: CircularProgressIndicator(strokeWidth: 2, valueColor: AlwaysStoppedAnimation<Color>(Colors.grey)),
          ),
        ),
      ),
      error: (err, stack) => const SizedBox(),
      data: (wikiData) {
        if (wikiData == null || wikiData['summary'] == null) return const SizedBox();

        final title = wikiData['title'] ?? topicTitle;
        final summary = wikiData['summary'] as String;
        final url = wikiData['url'] as String?;

        return Card(
          elevation: 0,
          color: Colors.blueGrey.shade50.withOpacity(0.6),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: BorderSide(color: Colors.blueGrey.shade100.withOpacity(0.5)),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(6),
                      decoration: const BoxDecoration(
                        color: Colors.white70,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(Icons.book, size: 20, color: Colors.blueGrey),
                    ),
                    const SizedBox(width: 10),
                    Text(
                      'Saiba mais com a Wikipedia',
                      style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 14, color: Colors.blueGrey.shade800),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Text(
                  title,
                  style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.black87),
                ),
                const SizedBox(height: 6),
                Text(
                  summary,
                  maxLines: 4,
                  overflow: TextOverflow.ellipsis,
                  style: GoogleFonts.inter(fontSize: 13, color: Colors.grey.shade800, height: 1.5),
                ),
                if (url != null) ...[
                  const SizedBox(height: 12),
                  InkWell(
                    onTap: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Abrindo link externo: $url'),
                          backgroundColor: Colors.blueGrey.shade800,
                        ),
                      );
                    },
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          'Ler artigo completo na Wikipedia',
                          style: GoogleFonts.inter(
                            color: Colors.blueAccent.shade700,
                            fontWeight: FontWeight.bold,
                            fontSize: 12,
                          ),
                        ),
                        const SizedBox(width: 4),
                        Icon(Icons.open_in_new, size: 12, color: Colors.blueAccent.shade700),
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildYouTubeSection(BuildContext context, WidgetRef ref, String topicTitle) {
    final youtubeAsync = ref.watch(youtubeVideosProvider(topicTitle));

    return youtubeAsync.when(
      loading: () => const Padding(
        padding: EdgeInsets.symmetric(vertical: 16.0),
        child: Center(
          child: SizedBox(
            height: 24,
            width: 24,
            child: CircularProgressIndicator(strokeWidth: 2, valueColor: AlwaysStoppedAnimation<Color>(Colors.red)),
          ),
        ),
      ),
      error: (err, stack) => const SizedBox(),
      data: (videos) {
        if (videos.isEmpty) return const SizedBox();

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 24),
            Row(
              children: [
                const Icon(Icons.play_circle_fill, color: Colors.red, size: 24),
                const SizedBox(width: 8),
                Text(
                  'Videoaulas Recomendadas',
                  style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 16, color: const Color(0xFF2C3E50)),
                ),
              ],
            ),
            const SizedBox(height: 12),
            SizedBox(
              height: 155,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: videos.length,
                itemBuilder: (context, index) {
                  final video = videos[index];
                  return Container(
                    width: 200,
                    margin: const EdgeInsets.only(right: 16),
                    child: Card(
                      elevation: 1,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      clipBehavior: Clip.antiAlias,
                      child: InkWell(
                        onTap: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text('Abrindo videoaula no YouTube: ${video.videoUrl}'),
                              backgroundColor: Colors.red.shade700,
                            ),
                          );
                        },
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Expanded(
                              child: Stack(
                                children: [
                                  Image.network(
                                    video.thumbnail,
                                    width: double.infinity,
                                    fit: BoxFit.cover,
                                    errorBuilder: (context, error, stackTrace) {
                                      return Container(
                                        color: Colors.grey.shade200,
                                        child: const Center(child: Icon(Icons.videocam, color: Colors.grey)),
                                      );
                                    },
                                  ),
                                  const Align(
                                    alignment: Alignment.center,
                                    child: CircleAvatar(
                                      backgroundColor: Colors.black54,
                                      radius: 16,
                                      child: Icon(Icons.play_arrow, color: Colors.white, size: 18),
                                    ),
                                  )
                                ],
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: Text(
                                video.title,
                                maxLines: 2,
                                overflow: TextOverflow.ellipsis,
                                style: GoogleFonts.inter(fontSize: 11, fontWeight: FontWeight.w600, color: Colors.black87),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        );
      },
    );
  }
}
