import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import 'package:go_router/go_router.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../application/course_repository.dart';
import '../domain/course_models.dart';
import '../../gamification/application/progress_repository.dart';
import '../../ai/application/ai_repository.dart';

class QuizScreen extends ConsumerStatefulWidget {
  final String topicId;
  const QuizScreen({super.key, required this.topicId});

  @override
  ConsumerState<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends ConsumerState<QuizScreen> {
  int _currentIndex = 0;
  String? _selectedOption;
  bool _hasAnswered = false;

  void _submitAnswer(Question question) async {
    if (_selectedOption == null) return;
    
    final isCorrect = _selectedOption == question.correctOption;
    
    // Anima a UI imediatamente
    setState(() {
      _hasAnswered = true;
    });

    // Registra silenciosamente no backend
    try {
      final repo = ref.read(progressRepositoryProvider);
      await repo.recordAttempt(question.id, isCorrect);
      
      // Força a atualização do XP global
      ref.invalidate(progressSummaryProvider);
      
      if (isCorrect && mounted) {
         ScaffoldMessenger.of(context).showSnackBar(
           SnackBar(
             content: Row(
               children: [
                 const Icon(Icons.star, color: Colors.yellow),
                 const SizedBox(width: 8),
                 Text('+10 XP Ganho!', style: GoogleFonts.inter(fontWeight: FontWeight.bold)),
               ],
             ),
             backgroundColor: Colors.green.shade800,
             duration: const Duration(seconds: 2),
             behavior: SnackBarBehavior.floating,
           )
         );
      }
    } catch (e) {
      debugPrint("Erro ao salvar progresso: $e");
    }
  }

  void _showAiExplanation(Question question, String selectedOption) async {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (ctx) {
        return Container(
          height: MediaQuery.of(ctx).size.height * 0.75,
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Icon(Icons.auto_awesome, color: Colors.purple),
                  const SizedBox(width: 8),
                  Text('IA Tutor (IMPARH)', style: GoogleFonts.inter(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.purple.shade900)),
                ],
              ),
              const Divider(),
              Expanded(
                child: FutureBuilder(
                  future: ref.read(aiRepositoryProvider).explainQuestion(question.id, selectedOption),
                  builder: (ctx, snapshot) {
                    if (snapshot.connectionState == ConnectionState.waiting) {
                      return Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const CircularProgressIndicator(color: Colors.purple),
                          const SizedBox(height: 16),
                          Text('O IA Tutor está analisando a questão...', style: GoogleFonts.inter(color: Colors.grey)),
                        ],
                      );
                    }
                    if (snapshot.hasError) {
                      return Center(child: Text('Erro: ${snapshot.error}', style: const TextStyle(color: Colors.red)));
                    }
                    return Markdown(
                      data: snapshot.data!.explanationMarkdown,
                      styleSheet: MarkdownStyleSheet(
                        p: GoogleFonts.inter(fontSize: 16, height: 1.5),
                        h3: GoogleFonts.inter(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.purple.shade800),
                        blockquoteDecoration: BoxDecoration(
                          color: Colors.purple.shade50,
                          border: Border(left: BorderSide(color: Colors.purple.shade300, width: 4)),
                        ),
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  void _nextQuestion(List<Question> questions) {
    if (_currentIndex < questions.length - 1) {
      setState(() {
        _currentIndex++;
        _selectedOption = null;
        _hasAnswered = false;
      });
    } else {
      // Fim do quiz
      context.pop();
    }
  }

  @override
  Widget build(BuildContext context) {
    final topicAsync = ref.watch(topicDetailProvider(widget.topicId));

    return Scaffold(
      backgroundColor: Colors.grey.shade50,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        foregroundColor: Colors.black87,
        title: Text('Simulado', style: GoogleFonts.inter(fontWeight: FontWeight.bold)),
      ),
      body: topicAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Erro: $err')),
        data: (topic) {
          if (topic.questions.isEmpty) return const Center(child: Text('Sem questões.'));
          
          final question = topic.questions[_currentIndex];
          final options = {
            'A': question.optionA,
            'B': question.optionB,
            'C': question.optionC,
            'D': question.optionD,
          };

          final isCorrect = _selectedOption == question.correctOption;

          return Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  'Questão ${_currentIndex + 1} de ${topic.questions.length}',
                  style: GoogleFonts.inter(color: Colors.grey.shade600, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 16),
                Text(
                  question.statement,
                  style: GoogleFonts.inter(fontSize: 18, height: 1.5),
                ),
                const SizedBox(height: 32),
                ...options.entries.map((entry) {
                  final key = entry.key;
                  final value = entry.value;

                  Color bgColor = Colors.white;
                  Color borderColor = Colors.grey.shade300;
                  
                  if (_hasAnswered) {
                    if (key == question.correctOption) {
                      bgColor = Colors.green.shade50;
                      borderColor = Colors.green;
                    } else if (key == _selectedOption) {
                      bgColor = Colors.red.shade50;
                      borderColor = Colors.red;
                    }
                  } else if (_selectedOption == key) {
                    bgColor = Colors.blue.shade50;
                    borderColor = Colors.blueAccent;
                  }

                  return Padding(
                    padding: const EdgeInsets.only(bottom: 12.0),
                    child: InkWell(
                      onTap: _hasAnswered ? null : () {
                        setState(() {
                          _selectedOption = key;
                        });
                      },
                      borderRadius: BorderRadius.circular(12),
                      child: Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: bgColor,
                          border: Border.all(color: borderColor, width: 2),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Row(
                          children: [
                            Text(
                              '$key) ',
                              style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 16),
                            ),
                            Expanded(
                              child: Text(value, style: GoogleFonts.inter(fontSize: 16)),
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                }),
                const Spacer(),
                if (_hasAnswered)
                  Container(
                    padding: const EdgeInsets.all(16),
                    margin: const EdgeInsets.only(bottom: 24),
                    decoration: BoxDecoration(
                      color: isCorrect ? Colors.green.shade50 : Colors.red.shade50,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: isCorrect ? Colors.green : Colors.red),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          isCorrect ? question.justificationCorrect : question.justificationIncorrect,
                          style: GoogleFonts.inter(
                            color: isCorrect ? Colors.green.shade900 : Colors.red.shade900,
                          ),
                        ),
                        if (!isCorrect) ...[
                          const SizedBox(height: 16),
                          SizedBox(
                            width: double.infinity,
                            child: OutlinedButton.icon(
                              style: OutlinedButton.styleFrom(
                                foregroundColor: Colors.purple.shade700,
                                side: BorderSide(color: Colors.purple.shade300),
                                padding: const EdgeInsets.symmetric(vertical: 12),
                              ),
                              icon: const Icon(Icons.auto_awesome),
                              label: const Text('Não entendi, me explique melhor 🤖'),
                              onPressed: () => _showAiExplanation(question, _selectedOption!),
                            ),
                          ),
                        ]
                      ],
                    ),
                  ),
                SizedBox(
                  height: 56,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: _hasAnswered 
                        ? Colors.blueAccent 
                        : (_selectedOption != null ? Colors.orange.shade600 : Colors.grey.shade300),
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                    ),
                    onPressed: () {
                      if (!_hasAnswered && _selectedOption != null) {
                        _submitAnswer(question);
                      } else if (_hasAnswered) {
                        _nextQuestion(topic.questions);
                      }
                    },
                    child: Text(
                      _hasAnswered ? 'CONTINUAR' : 'RESPONDER',
                      style: GoogleFonts.inter(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                  ),
                )
              ],
            ),
          );
        },
      ),
    );
  }
}
