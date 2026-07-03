import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import '../application/activity_log_repository.dart';
import '../domain/activity_log_models.dart';

class ActivityHistoryScreen extends ConsumerWidget {
  const ActivityHistoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final logsAsync = ref.watch(activityLogsProvider);

    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FA),
      appBar: AppBar(
        title: Text(
          'Meu Histórico',
          style: GoogleFonts.inter(fontWeight: FontWeight.bold, color: Colors.white),
        ),
        centerTitle: true,
        backgroundColor: const Color(0xFF203A43),
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: Colors.white),
            onPressed: () {
              ref.invalidate(activityLogsProvider);
            },
          )
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(activityLogsProvider);
        },
        child: logsAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, stack) => Center(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline, size: 60, color: Colors.redAccent),
                  const SizedBox(height: 16),
                  Text(
                    'Erro ao carregar histórico',
                    style: GoogleFonts.inter(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  Text('$err', textAlign: TextAlign.center, style: const TextStyle(color: Colors.grey)),
                ],
              ),
            ),
          ),
          data: (logs) {
            if (logs.isEmpty) {
              return ListView(
                physics: const AlwaysScrollableScrollPhysics(),
                children: [
                  SizedBox(height: MediaQuery.of(context).size.height * 0.25),
                  Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.history_toggle_off, size: 80, color: Colors.grey.shade400),
                        const SizedBox(height: 16),
                        Text(
                          'Nenhuma atividade registrada',
                          style: GoogleFonts.inter(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: Colors.grey.shade700,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 40.0),
                          child: Text(
                            'Comece a estudar respondendo questões, revisando flashcards ou conversando com a IA para ver seu histórico aqui.',
                            textAlign: TextAlign.center,
                            style: GoogleFonts.inter(color: Colors.grey.shade500, height: 1.5),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              );
            }

            return ListView.builder(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 24),
              itemCount: logs.length,
              itemBuilder: (context, index) {
                final log = logs[index];
                return _buildTimelineItem(context, log, index == 0, index == logs.length - 1);
              },
            );
          },
        ),
      ),
    );
  }

  Widget _buildTimelineItem(BuildContext context, ActivityLog log, bool isFirst, bool isLast) {
    final iconData = _getIcon(log.action, log.details);
    final color = _getColor(log.action, log.details);

    return IntrinsicHeight(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Timeline line and dot column
          Column(
            children: [
              Container(
                width: 2,
                height: 16,
                color: isFirst ? Colors.transparent : Colors.grey.shade300,
              ),
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.12),
                  shape: BoxShape.circle,
                  border: Border.all(color: color, width: 2),
                ),
                child: Icon(iconData, size: 20, color: color),
              ),
              Expanded(
                child: Container(
                  width: 2,
                  color: isLast ? Colors.transparent : Colors.grey.shade300,
                ),
              ),
            ],
          ),
          const SizedBox(width: 16),
          // Content Card
          Expanded(
            child: Container(
              margin: const EdgeInsets.only(bottom: 20),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.03),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
                border: Border.all(color: Colors.grey.shade100),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        _getActionTitle(log.action, log.details),
                        style: GoogleFonts.inter(
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                          color: const Color(0xFF2C3E50),
                        ),
                      ),
                      Text(
                        _formatTime(log.createdAt),
                        style: GoogleFonts.inter(
                          fontSize: 12,
                          color: Colors.grey.shade500,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    log.details ?? '',
                    style: GoogleFonts.inter(
                      fontSize: 14,
                      color: Colors.grey.shade700,
                      height: 1.4,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  IconData _getIcon(String action, String? details) {
    switch (action) {
      case 'SUBMIT_ANSWER':
        if (details != null && details.contains('corretamente')) {
          return Icons.check_circle_outline;
        }
        return Icons.highlight_off;
      case 'ASK_AI':
        return Icons.smart_toy_outlined;
      case 'VIEW_TOPIC':
        return Icons.auto_stories_outlined;
      case 'STUDY_FLASHCARDS':
        return Icons.style_outlined;
      default:
        return Icons.info_outline;
    }
  }

  Color _getColor(String action, String? details) {
    switch (action) {
      case 'SUBMIT_ANSWER':
        if (details != null && details.contains('corretamente')) {
          return const Color(0xFF2ECC71); // Green
        }
        return const Color(0xFFE74C3C); // Red
      case 'ASK_AI':
        return const Color(0xFF3498DB); // Blue
      case 'VIEW_TOPIC':
        return const Color(0xFFF39C12); // Orange
      case 'STUDY_FLASHCARDS':
        return const Color(0xFF9B59B6); // Purple
      default:
        return Colors.blueGrey;
    }
  }

  String _getActionTitle(String action, String? details) {
    switch (action) {
      case 'SUBMIT_ANSWER':
        if (details != null && details.contains('corretamente')) {
          return 'Questão Respondida (Acerto)';
        }
        return 'Questão Respondida (Erro)';
      case 'ASK_AI':
        return 'Ajuda da IA';
      case 'VIEW_TOPIC':
        return 'Leitura Teórica';
      case 'STUDY_FLASHCARDS':
        return 'Revisão Concluída';
      default:
        return 'Ação';
    }
  }

  String _formatTime(DateTime date) {
    final localDate = date.toLocal();
    final hour = localDate.hour.toString().padLeft(2, '0');
    final minute = localDate.minute.toString().padLeft(2, '0');
    final day = localDate.day.toString().padLeft(2, '0');
    final month = localDate.month.toString().padLeft(2, '0');
    return '$day/$month às $hour:$minute';
  }
}
