import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import '../application/course_repository.dart';
import '../domain/course_models.dart';
import '../../gamification/application/activity_log_repository.dart';

class FlashcardScreen extends ConsumerStatefulWidget {
  final String topicId;
  const FlashcardScreen({super.key, required this.topicId});

  @override
  ConsumerState<FlashcardScreen> createState() => _FlashcardScreenState();
}

class _FlashcardScreenState extends ConsumerState<FlashcardScreen> {
  int _currentIndex = 0;
  bool _showBack = false;

  void _flipCard() {
    setState(() {
      _showBack = !_showBack;
    });
  }

  void _nextCard(List<Flashcard> flashcards) {
    if (_currentIndex < flashcards.length - 1) {
      setState(() {
        _currentIndex++;
        _showBack = false;
      });
    } else {
      // Registrar log de finalização
      try {
        ref.read(activityLogRepositoryProvider).recordActivityLog(
          'STUDY_FLASHCARDS',
          'Estudou ${flashcards.length} flashcards',
        );
      } catch (_) {}
      context.pop();
    }
  }

  Widget _buildCard(Flashcard fc) {
    return GestureDetector(
      onTap: _flipCard,
      child: AnimatedSwitcher(
        duration: const Duration(milliseconds: 500),
        transitionBuilder: (Widget child, Animation<double> animation) {
          final rotateAnim = Tween(begin: pi, end: 0.0).animate(animation);
          return AnimatedBuilder(
            animation: rotateAnim,
            child: child,
            builder: (context, widget) {
              final isUnder = (ValueKey(_showBack) != widget?.key);
              final value = isUnder ? min(rotateAnim.value, pi / 2) : rotateAnim.value;
              return Transform(
                transform: Matrix4.rotationY(value)..setEntry(3, 2, 0.001),
                alignment: Alignment.center,
                child: widget,
              );
            },
          );
        },
        child: _showBack ? _buildBackSide(fc.back) : _buildFrontSide(fc.front),
      ),
    );
  }

  Widget _buildFrontSide(String text) {
    return Container(
      key: const ValueKey(false),
      width: double.infinity,
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 10, offset: Offset(0, 5))],
      ),
      child: Center(
        child: Text(
          text,
          textAlign: TextAlign.center,
          style: GoogleFonts.inter(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.blueGrey.shade900),
        ),
      ),
    );
  }

  Widget _buildBackSide(String text) {
    return Container(
      key: const ValueKey(true),
      width: double.infinity,
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: Colors.deepPurple.shade50,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: Colors.deepPurple.shade200, width: 2),
        boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 10, offset: Offset(0, 5))],
      ),
      child: Center(
        child: Text(
          text,
          textAlign: TextAlign.center,
          style: GoogleFonts.inter(fontSize: 20, color: Colors.deepPurple.shade900),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final fcAsync = ref.watch(topicFlashcardsProvider(widget.topicId));

    return Scaffold(
      backgroundColor: Colors.grey.shade100,
      appBar: AppBar(
        title: Text('Revisão Rápida', style: GoogleFonts.inter(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.transparent,
        foregroundColor: Colors.black87,
        elevation: 0,
      ),
      body: fcAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, st) => Center(child: Text('Erro: $e')),
        data: (flashcards) {
          if (flashcards.isEmpty) return const Center(child: Text('Nenhum flashcard disponível.'));

          final fc = flashcards[_currentIndex];

          return Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  'Card ${_currentIndex + 1} de ${flashcards.length}',
                  textAlign: TextAlign.center,
                  style: GoogleFonts.inter(fontWeight: FontWeight.bold, color: Colors.grey),
                ),
                const SizedBox(height: 32),
                Expanded(child: _buildCard(fc)),
                const SizedBox(height: 48),
                if (_showBack) ...[
                  Row(
                    children: [
                      Expanded(
                        child: OutlinedButton(
                          style: OutlinedButton.styleFrom(
                            foregroundColor: Colors.red,
                            side: const BorderSide(color: Colors.red),
                            padding: const EdgeInsets.symmetric(vertical: 16),
                          ),
                          onPressed: () => _nextCard(flashcards),
                          child: const Text('NÃO LEMBREI', style: TextStyle(fontWeight: FontWeight.bold)),
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(vertical: 16),
                          ),
                          onPressed: () => _nextCard(flashcards),
                          child: const Text('LEMBREI', style: TextStyle(fontWeight: FontWeight.bold)),
                        ),
                      ),
                    ],
                  ),
                ] else ...[
                  const Center(child: Text('Toque no card para virar 👆', style: TextStyle(color: Colors.grey))),
                ],
              ],
            ),
          );
        },
      ),
    );
  }
}
