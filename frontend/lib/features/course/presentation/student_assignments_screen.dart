import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import '../application/classroom_repository.dart';
import '../domain/classroom_models.dart';

class StudentAssignmentsScreen extends ConsumerStatefulWidget {
  const StudentAssignmentsScreen({super.key});

  @override
  ConsumerState<StudentAssignmentsScreen> createState() => _StudentAssignmentsScreenState();
}

class _StudentAssignmentsScreenState extends ConsumerState<StudentAssignmentsScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade50,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: const Color(0xFF1F4068),
        title: Text(
          'Minhas Redações & Tarefas',
          style: GoogleFonts.inter(fontWeight: FontWeight.bold, color: Colors.white),
        ),
        bottom: TabBar(
          controller: _tabController,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.grey.shade400,
          indicatorColor: Colors.blueAccent.shade200,
          labelStyle: GoogleFonts.inter(fontWeight: FontWeight.w600),
          tabs: const [
            Tab(text: 'Minhas Redações', icon: Icon(Icons.history_edu)),
            Tab(text: 'Turmas & Tarefas', icon: Icon(Icons.class_)),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildMyEssaysTab(),
          _buildClassroomsTab(),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: const Color(0xFFE94560),
        onPressed: () {
          context.push('/student/essay/write');
        },
        icon: const Icon(Icons.edit_note, color: Colors.white),
        label: Text(
          'Treinar Redação',
          style: GoogleFonts.inter(fontWeight: FontWeight.bold, color: Colors.white),
        ),
      ),
    );
  }

  Widget _buildMyEssaysTab() {
    final essaysAsync = ref.watch(essaysProvider);

    return essaysAsync.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, stack) => Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Text(
            'Erro ao carregar redações: $err',
            style: GoogleFonts.inter(color: Colors.red),
            textAlign: TextAlign.center,
          ),
        ),
      ),
      data: (essays) {
        if (essays.isEmpty) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.edit_document, size: 64, color: Colors.grey.shade300),
                const SizedBox(height: 16),
                Text(
                  'Nenhuma redação enviada ainda.',
                  style: GoogleFonts.inter(fontSize: 16, color: Colors.grey.shade600, fontWeight: FontWeight.w500),
                ),
                const SizedBox(height: 8),
                Text(
                  'Clique no botão abaixo para começar a treinar!',
                  style: GoogleFonts.inter(fontSize: 14, color: Colors.grey.shade400),
                ),
              ],
            ),
          );
        }

        return RefreshIndicator(
          onRefresh: () async {
            ref.invalidate(essaysProvider);
          },
          child: ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: essays.length,
            itemBuilder: (context, index) {
              final essay = essays[index];
              return _buildEssayCard(essay);
            },
          ),
        );
      },
    );
  }

  Widget _buildEssayCard(StudentEssay essay) {
    Color statusColor;
    String statusLabel;

    switch (essay.status) {
      case 'draft':
        statusColor = Colors.grey;
        statusLabel = 'Rascunho';
        break;
      case 'submitted':
        statusColor = Colors.orange;
        statusLabel = 'Enviado';
        break;
      case 'reviewed':
        statusColor = Colors.blue;
        statusLabel = 'Corrigido por IA';
        break;
      case 'graded':
        statusColor = Colors.green;
        statusLabel = 'Avaliado por Professor';
        break;
      default:
        statusColor = Colors.blue;
        statusLabel = 'Corrigido';
    }

    return Card(
      elevation: 2,
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ExpansionTile(
        tilePadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: Colors.blueAccent.shade100.withOpacity(0.2),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.article, color: Color(0xFF1F4068)),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    essay.assignmentId != null ? 'Tarefa de Redação' : 'Prática Livre',
                    style: GoogleFonts.inter(fontSize: 12, fontWeight: FontWeight.w600, color: Colors.grey.shade500),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    'Redação #${essay.id.substring(0, 5)}',
                    style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 16, color: const Color(0xFF162447)),
                  ),
                ],
              ),
            ),
          ],
        ),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: statusColor.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  statusLabel,
                  style: GoogleFonts.inter(color: statusColor, fontWeight: FontWeight.bold, fontSize: 11),
                ),
              ),
              if (essay.grade != null)
                Text(
                  'Nota: ${essay.grade!.toStringAsFixed(1)}',
                  style: GoogleFonts.inter(fontWeight: FontWeight.bold, color: Colors.green.shade800, fontSize: 14),
                )
              else
                Text(
                  'Aguardando nota',
                  style: GoogleFonts.inter(color: Colors.grey.shade600, fontSize: 12, fontStyle: FontStyle.italic),
                ),
            ],
          ),
        ),
        children: [
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Divider(),
                const SizedBox(height: 8),
                Text(
                  'Texto Enviado:',
                  style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 14, color: const Color(0xFF1F4068)),
                ),
                const SizedBox(height: 6),
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.grey.shade100,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.grey.shade300),
                  ),
                  child: Text(
                    essay.content,
                    style: GoogleFonts.inter(fontSize: 14, fontStyle: FontStyle.italic, color: Colors.black87),
                  ),
                ),
                const SizedBox(height: 16),
                if (essay.aiFeedback != null) ...[
                  Row(
                    children: [
                      const Icon(Icons.psychology, color: Colors.indigo),
                      const SizedBox(width: 6),
                      Text(
                        'Feedback do Tutor de IA:',
                        style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 14, color: Colors.indigo),
                      ),
                    ],
                  ),
                  const SizedBox(height: 6),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.indigo.shade50.withOpacity(0.5),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.indigo.shade100),
                    ),
                    child: Text(
                      essay.aiFeedback!,
                      style: GoogleFonts.inter(fontSize: 14, color: Colors.indigo.shade900),
                    ),
                  ),
                  const SizedBox(height: 16),
                ],
                if (essay.teacherFeedback != null && essay.teacherFeedback!.isNotEmpty) ...[
                  Row(
                    children: [
                      const Icon(Icons.person, color: Colors.teal),
                      const SizedBox(width: 6),
                      Text(
                        'Observações do Professor:',
                        style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 14, color: Colors.teal),
                      ),
                    ],
                  ),
                  const SizedBox(height: 6),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.teal.shade50.withOpacity(0.5),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.teal.shade100),
                    ),
                    child: Text(
                      essay.teacherFeedback!,
                      style: GoogleFonts.inter(fontSize: 14, color: Colors.teal.shade900),
                    ),
                  ),
                ],
              ],
            ),
          )
        ],
      ),
    );
  }

  Widget _buildClassroomsTab() {
    final classroomsAsync = ref.watch(classroomsProvider);

    return classroomsAsync.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (err, stack) => Center(child: Text('Erro ao carregar turmas: $err')),
      data: (classrooms) {
        if (classrooms.isEmpty) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.class_outlined, size: 64, color: Colors.grey.shade300),
                const SizedBox(height: 16),
                Text(
                  'Nenhuma turma disponível no momento.',
                  style: GoogleFonts.inter(fontSize: 16, color: Colors.grey.shade600, fontWeight: FontWeight.w500),
                ),
                const SizedBox(height: 8),
                Text(
                  'Professores podem criar turmas no Painel.',
                  style: GoogleFonts.inter(fontSize: 14, color: Colors.grey.shade400),
                ),
              ],
            ),
          );
        }

        return RefreshIndicator(
          onRefresh: () async {
            ref.invalidate(classroomsProvider);
          },
          child: ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: classrooms.length,
            itemBuilder: (context, index) {
              final classroom = classrooms[index];
              return _buildClassroomItem(classroom);
            },
          ),
        );
      },
    );
  }

  Widget _buildClassroomItem(ClassRoom classroom) {
    return Card(
      elevation: 1,
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ExpansionTile(
        tilePadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
        leading: Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: Colors.blueAccent.shade100.withOpacity(0.2),
            shape: BoxShape.circle,
          ),
          child: Icon(Icons.school, color: Colors.blue.shade800),
        ),
        title: Text(
          classroom.name,
          style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 16, color: const Color(0xFF162447)),
        ),
        subtitle: Text(
          'Nível: ${classroom.level} • Série: ${classroom.series}º Ano',
          style: GoogleFonts.inter(fontSize: 12, color: Colors.grey.shade600),
        ),
        children: [
          _ClassroomAssignmentsList(classroomId: classroom.id),
        ],
      ),
    );
  }
}

class _ClassroomAssignmentsList extends ConsumerWidget {
  final String classroomId;
  const _ClassroomAssignmentsList({required this.classroomId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final assignmentsAsync = ref.watch(classroomAssignmentsProvider(classroomId));

    return assignmentsAsync.when(
      loading: () => const Padding(
        padding: EdgeInsets.all(16.0),
        child: Center(child: SizedBox(height: 24, width: 24, child: CircularProgressIndicator(strokeWidth: 2))),
      ),
      error: (err, stack) => Padding(
        padding: const EdgeInsets.all(16.0),
        child: Text('Erro: $err', style: const TextStyle(color: Colors.red)),
      ),
      data: (assignments) {
        if (assignments.isEmpty) {
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 24.0, horizontal: 16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.assignment_turned_in, size: 20, color: Colors.grey.shade400),
                const SizedBox(width: 8),
                Text(
                  'Nenhuma tarefa pendente nesta turma.',
                  style: GoogleFonts.inter(color: Colors.grey.shade500, fontStyle: FontStyle.italic),
                ),
              ],
            ),
          );
        }

        return Container(
          color: Colors.grey.shade50,
          child: Column(
            children: [
              Padding(
                padding: const EdgeInsets.only(left: 20.0, top: 12.0, bottom: 4.0),
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    'TAREFAS DISPONÍVEIS:',
                    style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 11, color: Colors.grey.shade700),
                  ),
                ),
              ),
              ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: assignments.length,
                itemBuilder: (context, index) {
                  final assignment = assignments[index];
                  return Column(
                    children: [
                      ListTile(
                        contentPadding: const EdgeInsets.symmetric(horizontal: 24, vertical: 4),
                        title: Text(
                          assignment.title,
                          style: GoogleFonts.inter(fontWeight: FontWeight.w600, fontSize: 14),
                        ),
                        subtitle: Text(
                          assignment.description ?? 'Sem descrição.',
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: GoogleFonts.inter(fontSize: 12),
                        ),
                        trailing: ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF1F4068),
                            foregroundColor: Colors.white,
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                          ),
                          onPressed: () {
                            context.push('/student/essay/write?assignmentId=${assignment.id}');
                          },
                          child: Text(
                            'Enviar',
                            style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 12),
                          ),
                        ),
                      ),
                      if (index < assignments.length - 1) const Divider(indent: 24, endIndent: 24),
                    ],
                  );
                },
              ),
              const SizedBox(height: 12),
            ],
          ),
        );
      },
    );
  }
}

// --- TELA DE ESCRITA DE REDAÇÃO ---

class StudentWriteEssayScreen extends ConsumerStatefulWidget {
  final String? assignmentId;
  const StudentWriteEssayScreen({super.key, this.assignmentId});

  @override
  ConsumerState<StudentWriteEssayScreen> createState() => _StudentWriteEssayScreenState();
}

class _StudentWriteEssayScreenState extends ConsumerState<StudentWriteEssayScreen> {
  final TextEditingController _textController = TextEditingController();
  int _wordCount = 0;
  bool _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    _textController.addListener(_updateWordCount);
  }

  @override
  void dispose() {
    _textController.removeListener(_updateWordCount);
    _textController.dispose();
    super.dispose();
  }

  void _updateWordCount() {
    final text = _textController.text.trim();
    if (text.isEmpty) {
      setState(() {
        _wordCount = 0;
      });
      return;
    }
    setState(() {
      _wordCount = text.split(RegExp(r'\s+')).length;
    });
  }

  Future<void> _submitEssay() async {
    if (_wordCount < 15) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('A redação precisa conter no mínimo 15 palavras para ser corrigida!'),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    setState(() {
      _isSubmitting = true;
    });

    try {
      final repo = ref.read(classroomRepositoryProvider);
      final essay = await repo.submitEssay(_textController.text, assignmentId: widget.assignmentId);

      // Recarrega lista
      ref.invalidate(essaysProvider);

      if (mounted) {
        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (context) => AlertDialog(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            title: Row(
              children: const [
                Icon(Icons.check_circle, color: Colors.green),
                SizedBox(width: 8),
                Text('Redação Corrigida!'),
              ],
            ),
            content: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Sua redação foi analisada com sucesso pela nossa IA.',
                    style: GoogleFonts.inter(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    'Nota sugerida pela IA: ${essay.grade?.toStringAsFixed(1) ?? "N/A"}',
                    style: GoogleFonts.inter(color: Colors.green.shade800, fontWeight: FontWeight.bold, fontSize: 16),
                  ),
                  const SizedBox(height: 12),
                  const Divider(),
                  const SizedBox(height: 8),
                  Text(
                    'Feedback do Tutor:',
                    style: GoogleFonts.inter(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    essay.aiFeedback ?? 'Sem feedback gerado.',
                    style: GoogleFonts.inter(fontSize: 14),
                  ),
                ],
              ),
            ),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context); // fecha dialog
                  context.pop(); // volta para tela anterior
                },
                child: const Text('Entendido'),
              )
            ],
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Erro ao enviar redação: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isSubmitting = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: const Color(0xFF1F4068),
        foregroundColor: Colors.white,
        title: Text(
          widget.assignmentId != null ? 'Responder Tarefa' : 'Treino de Redação',
          style: GoogleFonts.inter(fontWeight: FontWeight.bold),
        ),
      ),
      body: _isSubmitting
          ? Center(
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const CircularProgressIndicator(valueColor: AlwaysStoppedAnimation<Color>(Color(0xFFE94560))),
                    const SizedBox(height: 24),
                    Text(
                      'Tutor de IA está corrigindo...',
                      style: GoogleFonts.inter(fontSize: 18, fontWeight: FontWeight.bold, color: const Color(0xFF1F4068)),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Analisando coesão, concordância, ortografia e riqueza de vocabulário. Isso pode levar alguns segundos.',
                      textAlign: TextAlign.center,
                      style: GoogleFonts.inter(color: Colors.grey.shade600, fontSize: 13),
                    ),
                  ],
                ),
              ),
            )
          : SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Instruções:',
                    style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 16, color: const Color(0xFF162447)),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    widget.assignmentId != null
                        ? 'Escreva seu texto em resposta à proposta da tarefa acima. A redação deve ter pelo menos 15 palavras.'
                        : 'Escreva sobre o tema de sua preferência. Nosso Tutor IA fará uma correção detalhada com base nas competências de escrita do ENEM.',
                    style: GoogleFonts.inter(color: Colors.grey.shade700, fontSize: 14),
                  ),
                  const SizedBox(height: 20),
                  Container(
                    decoration: BoxDecoration(
                      color: Colors.grey.shade50,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: Colors.grey.shade300),
                    ),
                    child: Column(
                      children: [
                        TextField(
                          controller: _textController,
                          maxLines: 15,
                          minLines: 8,
                          style: GoogleFonts.inter(fontSize: 15),
                          decoration: InputDecoration(
                            hintText: 'Comece a digitar seu texto aqui...',
                            hintStyle: GoogleFonts.inter(color: Colors.grey.shade400),
                            contentPadding: const EdgeInsets.all(16),
                            border: InputBorder.none,
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                          decoration: BoxDecoration(
                            color: Colors.grey.shade100,
                            borderRadius: const BorderRadius.only(
                              bottomLeft: Radius.circular(16),
                              bottomRight: Radius.circular(16),
                            ),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                '$_wordCount palavras',
                                style: GoogleFonts.inter(
                                  fontWeight: FontWeight.bold,
                                  color: _wordCount >= 15 ? Colors.green.shade700 : Colors.orange.shade700,
                                ),
                              ),
                              if (_wordCount < 15)
                                Text(
                                  'Mínimo: 15',
                                  style: GoogleFonts.inter(color: Colors.grey.shade500, fontSize: 12),
                                ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),
                  SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFFE94560),
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      onPressed: _submitEssay,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.rocket_launch),
                          const SizedBox(width: 8),
                          Text(
                            'Enviar para Correção IA',
                            style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 16),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
