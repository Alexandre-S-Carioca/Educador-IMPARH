import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import '../application/admin_repository.dart';
import '../../course/application/course_repository.dart';

class AdminTopicFormScreen extends ConsumerStatefulWidget {
  final String unitId;
  const AdminTopicFormScreen({super.key, required this.unitId});

  @override
  ConsumerState<AdminTopicFormScreen> createState() => _AdminTopicFormScreenState();
}

class _AdminTopicFormScreenState extends ConsumerState<AdminTopicFormScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  final _introController = TextEditingController();
  final _markdownController = TextEditingController();
  bool _isLoading = false;

  void _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      final repo = ref.read(adminRepositoryProvider);
      await repo.createTopic(widget.unitId, {
        "title": _titleController.text,
        "difficulty": 1,
        "order_index": 1,
        "introduction": _introController.text,
        "theory_markdown": _markdownController.text,
      });

      // Recarrega os módulos para exibir o novo tópico na tela
      ref.invalidate(modulesProvider);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Tópico criado com sucesso!'), backgroundColor: Colors.green),
        );
        context.pop();
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Erro: $e'), backgroundColor: Colors.red));
      }
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Novo Tópico'),
        backgroundColor: Colors.blueGrey.shade900,
        foregroundColor: Colors.white,
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(24),
          children: [
            TextFormField(
              controller: _titleController,
              decoration: const InputDecoration(labelText: 'Título do Tópico (Ex: 2.1 Sintaxe)', border: OutlineInputBorder()),
              validator: (v) => v!.isEmpty ? 'Obrigatório' : null,
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _introController,
              decoration: const InputDecoration(labelText: 'Introdução Breve', border: OutlineInputBorder()),
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _markdownController,
              maxLines: 15,
              decoration: const InputDecoration(
                labelText: 'Teoria (Suporta Markdown)', 
                border: OutlineInputBorder(),
                hintText: '# Título Grande\n**Negrito** e *Itálico*',
              ),
            ),
            const SizedBox(height: 32),
            SizedBox(
              height: 56,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.blueGrey.shade900, foregroundColor: Colors.white),
                onPressed: _isLoading ? null : _submit,
                child: _isLoading ? const CircularProgressIndicator(color: Colors.white) : const Text('SALVAR TÓPICO', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            )
          ],
        ),
      ),
    );
  }
}
