import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import '../application/progress_repository.dart';

class StatisticsScreen extends ConsumerWidget {
  const StatisticsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final statsAsync = ref.watch(userStatisticsProvider);
    final summaryAsync = ref.watch(progressSummaryProvider);

    return Scaffold(
      backgroundColor: Colors.grey.shade50,
      appBar: AppBar(
        title: Text('Meu Desempenho', style: GoogleFonts.inter(fontWeight: FontWeight.bold, color: Colors.black87)),
        backgroundColor: Colors.white,
        elevation: 0,
        centerTitle: false,
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(userStatisticsProvider);
          ref.invalidate(progressSummaryProvider);
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Nível e XP
              summaryAsync.when(
                loading: () => const CircularProgressIndicator(),
                error: (e, st) => Text('Erro: $e'),
                data: (summary) {
                  return Container(
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      gradient: LinearGradient(colors: [Colors.purple.shade600, Colors.deepPurple.shade900]),
                      borderRadius: BorderRadius.circular(24),
                    ),
                    child: Row(
                      children: [
                        CircleAvatar(
                          radius: 32,
                          backgroundColor: Colors.white24,
                          child: Text('L${summary.level}', style: GoogleFonts.inter(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
                        ),
                        const SizedBox(width: 16),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Aluno Dedicado', style: GoogleFonts.inter(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
                            Text('${summary.totalXp} XP Acumulados', style: GoogleFonts.inter(fontSize: 16, color: Colors.purple.shade100)),
                          ],
                        )
                      ],
                    ),
                  );
                }
              ),
              const SizedBox(height: 32),
              
              Text('Estatísticas de Resolução', style: GoogleFonts.inter(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              
              // Estatísticas Vitais
              statsAsync.when(
                loading: () => const Center(child: CircularProgressIndicator()),
                error: (e, st) => Center(child: Text('Erro ao carregar estatísticas: $e')),
                data: (stats) {
                  return Column(
                    children: [
                      _buildAccuracyCard(stats.accuracyPercentage),
                      const SizedBox(height: 16),
                      Row(
                        children: [
                          Expanded(child: _buildStatCard('Resolvidas', stats.totalQuestions.toString(), Icons.assignment, Colors.blue)),
                          const SizedBox(width: 16),
                          Expanded(child: _buildStatCard('Acertos', stats.totalCorrect.toString(), Icons.check_circle, Colors.green)),
                        ],
                      ),
                      const SizedBox(height: 16),
                      Row(
                        children: [
                          Expanded(child: _buildStatCard('Erros', stats.totalIncorrect.toString(), Icons.cancel, Colors.red)),
                          const SizedBox(width: 16),
                          Expanded(child: _buildStatCard('Foco', 'IMPARH', Icons.account_balance, Colors.orange)),
                        ],
                      ),
                    ],
                  );
                }
              )
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAccuracyCard(double accuracy) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 10, offset: Offset(0, 4))],
      ),
      child: Column(
        children: [
          Text('Taxa de Acertos Global', style: GoogleFonts.inter(fontSize: 16, color: Colors.grey.shade600, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          Stack(
            alignment: Alignment.center,
            children: [
              SizedBox(
                width: 120,
                height: 120,
                child: CircularProgressIndicator(
                  value: accuracy / 100,
                  strokeWidth: 12,
                  backgroundColor: Colors.grey.shade200,
                  color: accuracy >= 70 ? Colors.green : (accuracy >= 50 ? Colors.orange : Colors.red),
                ),
              ),
              Text(
                '${accuracy.toStringAsFixed(1)}%',
                style: GoogleFonts.inter(fontSize: 28, fontWeight: FontWeight.bold),
              )
            ],
          ),
          const SizedBox(height: 16),
          Text(
            accuracy >= 70 ? 'Pronto para a posse! 🏆' : (accuracy >= 50 ? 'No caminho certo! 📚' : 'Precisa revisar mais! ⚠️'),
            style: GoogleFonts.inter(color: Colors.grey.shade800),
          )
        ],
      ),
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 4))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 28),
          const SizedBox(height: 12),
          Text(value, style: GoogleFonts.inter(fontSize: 24, fontWeight: FontWeight.bold)),
          Text(title, style: GoogleFonts.inter(fontSize: 14, color: Colors.grey.shade600)),
        ],
      ),
    );
  }
}
