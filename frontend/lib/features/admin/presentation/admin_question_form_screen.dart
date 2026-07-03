import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../application/admin_repository.dart';
import '../../course/application/course_repository.dart';

class AdminQuestionFormScreen extends ConsumerStatefulWidget {
  final String topicId;
  const AdminQuestionFormScreen({super.key, required this.topicId});

  @override
  ConsumerState<AdminQuestionFormScreen> createState() => _AdminQuestionFormScreenState();
}

class _AdminQuestionFormScreenState extends ConsumerState<AdminQuestionFormScreen> {
  final _formKey = GlobalKey<FormState>();
  final _statementCtrl = TextEditingController();
  final _optACtrl = TextEditingController();
  final _optBCtrl = TextEditingController();
  final _optCCtrl = TextEditingController();
  final _optDCtrl = TextEditingController();
  final _justCorrectCtrl = TextEditingController();
  final _justIncorrectCtrl = TextEditingController();
  String _correctOption = 'A';
  bool _isLoading = false;

  void _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _isLoading = true);

    try {
      final repo = ref.read(adminRepositoryProvider);
      await repo.createQuestion(widget.topicId, {
        "statement": _statementCtrl.text,
        "option_a": _optACtrl.text,
        "option_b": _optBCtrl.text,
        "option_c": _optCCtrl.text,
        "option_d": _optDCtrl.text,
        "correct_option": _correctOption,
        "justification_correct": _justCorrectCtrl.text,
        "justification_incorrect": _justIncorrectCtrl.text,
        "difficulty": 2,
        "subject": "Língua Portuguesa",
        "subsubject": "Geral",
        "board": "IMPARH"
      });

      // Limpa cache do tópico para a questão aparecer no app
      ref.invalidate(topicDetailProvider(widget.topicId));

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Questão salva!'), backgroundColor: Colors.green));
        context.pop();
      }
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Erro: $e'), backgroundColor: Colors.red));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Nova Questão IMPARH'), backgroundColor: Colors.blueGrey.shade900, foregroundColor: Colors.white),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(24),
          children: [
            TextFormField(controller: _statementCtrl, maxLines: 4, decoration: const InputDecoration(labelText: 'Enunciado da Questão', border: OutlineInputBorder()), validator: (v) => v!.isEmpty ? 'Obrigatório' : null),
            const SizedBox(height: 16),
            TextFormField(controller: _optACtrl, decoration: const InputDecoration(labelText: 'Opção A', border: OutlineInputBorder())),
            const SizedBox(height: 8),
            TextFormField(controller: _optBCtrl, decoration: const InputDecoration(labelText: 'Opção B', border: OutlineInputBorder())),
            const SizedBox(height: 8),
            TextFormField(controller: _optCCtrl, decoration: const InputDecoration(labelText: 'Opção C', border: OutlineInputBorder())),
            const SizedBox(height: 8),
            TextFormField(controller: _optDCtrl, decoration: const InputDecoration(labelText: 'Opção D', border: OutlineInputBorder())),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _correctOption,
              decoration: const InputDecoration(labelText: 'Alternativa Correta', border: OutlineInputBorder()),
              items: ['A', 'B', 'C', 'D'].map((e) => DropdownMenuItem(value: e, child: Text('Opção $e'))).toList(),
              onChanged: (v) => setState(() => _correctOption = v!),
            ),
            const SizedBox(height: 16),
            TextFormField(controller: _justCorrectCtrl, maxLines: 2, decoration: const InputDecoration(labelText: 'Justificativa (Acerto)', border: OutlineInputBorder())),
            const SizedBox(height: 8),
            TextFormField(controller: _justIncorrectCtrl, maxLines: 2, decoration: const InputDecoration(labelText: 'Justificativa (Erro)', border: OutlineInputBorder())),
            const SizedBox(height: 32),
            SizedBox(
              height: 56,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.blueGrey.shade900, foregroundColor: Colors.white),
                onPressed: _isLoading ? null : _submit,
                child: _isLoading ? const CircularProgressIndicator(color: Colors.white) : const Text('SALVAR QUESTÃO'),
              ),
            )
          ],
        ),
      ),
    );
  }
}
