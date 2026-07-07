import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import '../application/classroom_repository.dart';
import '../domain/classroom_models.dart';

class TeacherClassroomsScreen extends ConsumerStatefulWidget {
  const TeacherClassroomsScreen({super.key});

  @override
  ConsumerState<TeacherClassroomsScreen> createState() => _TeacherClassroomsScreenState();
}

class _TeacherClassroomsScreenState extends ConsumerState<TeacherClassroomsScreen> with SingleTickerProviderStateMixin {
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
      backgroundColor: Colors.blueGrey.shade50,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: const Color(0xFF2C3E50),
        title: Text(
          'Painel de Gestão do Professor',
          style: GoogleFonts.inter(fontWeight: FontWeight.bold, color: Colors.white),
        ),
        bottom: TabBar(
          controller: _tabController,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.grey.shade400,
          indicatorColor: Colors.tealAccent,
          labelStyle: GoogleFonts.inter(fontWeight: FontWeight.w600),
          tabs: const [
            Tab(text: 'Minhas Turmas', icon: Icon(Icons.school)),
            Tab(text: 'Corrigir Redações', icon: Icon(Icons.rate_review)),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildClassroomsTab(),
          _buildEssaysTab(),
        ],
      ),
    );
  }

  Widget _buildClassroomsTab() {
    final classroomsAsync = ref.watch(classroomsProvider);

    return Scaffold(
      backgroundColor: Colors.transparent,
      body: classroomsAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Erro ao carregar turmas: $err')),
        data: (classrooms) {
          if (classrooms.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.school_outlined, size: 64, color: Colors.grey.shade400),
                  const SizedBox(height: 16),
                  Text(
                    'Você não possui turmas cadastradas.',
                    style: GoogleFonts.inter(fontSize: 16, color: Colors.grey.shade600, fontWeight: FontWeight.w500),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Clique no botão abaixo para criar sua primeira turma!',
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
                return _buildClassroomCard(classroom);
              },
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        heroTag: 'btn_create_classroom',
        backgroundColor: const Color(0xFF1ABC9C),
        onPressed: _showCreateClassroomDialog,
        icon: const Icon(Icons.add, color: Colors.white),
        label: Text(
          'Nova Turma',
          style: GoogleFonts.inter(fontWeight: FontWeight.bold, color: Colors.white),
        ),
      ),
    );
  }

  Widget _buildClassroomCard(ClassRoom classroom) {
    return Card(
      elevation: 2,
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ExpansionTile(
        tilePadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
        leading: Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: Colors.teal.shade50,
            shape: BoxShape.circle,
          ),
          child: const Icon(Icons.group, color: Color(0xFF2C3E50)),
        ),
        title: Text(
          classroom.name,
          style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 18, color: const Color(0xFF2C3E50)),
        ),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 4.0),
          child: Text(
            'Nível: ${classroom.level} • ${classroom.series}º Ano',
            style: GoogleFonts.inter(fontSize: 13, color: Colors.grey.shade600),
          ),
        ),
        children: [
          Container(
            color: Colors.blueGrey.shade50.withOpacity(0.5),
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'Tarefas da Turma',
                      style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 14, color: const Color(0xFF2C3E50)),
                    ),
                    Row(
                      children: [
                        ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.indigo.shade600,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                          ),
                          onPressed: () => _showClassroomReport(classroom.id),
                          icon: const Icon(Icons.analytics, size: 16),
                          label: const Text('Relatório', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                        ),
                        const SizedBox(width: 8),
                        ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF2C3E50),
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                          ),
                          onPressed: () => _showCreateAssignmentDialog(classroom.id),
                          icon: const Icon(Icons.add, size: 16),
                          label: const Text('Tarefa', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                        ),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                _TeacherAssignmentsList(classroomId: classroom.id),
              ],
            ),
          )
        ],
      ),
    );
  }

  void _showCreateClassroomDialog() {
    final nameController = TextEditingController();
    String selectedLevel = 'FUNDAMENTAL_II';
    int selectedSeries = 9;

    showDialog(
      context: context,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setDialogState) {
            return AlertDialog(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              title: Text('Criar Nova Turma', style: GoogleFonts.inter(fontWeight: FontWeight.bold)),
              content: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    TextField(
                      controller: nameController,
                      decoration: const InputDecoration(
                        labelText: 'Nome da Turma (Ex: 9º Ano - Sala 102)',
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 16),
                    DropdownButtonFormField<String>(
                      value: selectedLevel,
                      decoration: const InputDecoration(
                        labelText: 'Nível de Ensino',
                        border: OutlineInputBorder(),
                      ),
                      items: const [
                        DropdownMenuItem(value: 'FUNDAMENTAL_I', child: Text('Fundamental I')),
                        DropdownMenuItem(value: 'FUNDAMENTAL_II', child: Text('Fundamental II')),
                        DropdownMenuItem(value: 'HIGH_SCHOOL', child: Text('Ensino Médio')),
                      ],
                      onChanged: (val) {
                        if (val != null) {
                          setDialogState(() {
                            selectedLevel = val;
                          });
                        }
                      },
                    ),
                    const SizedBox(height: 16),
                    DropdownButtonFormField<int>(
                      value: selectedSeries,
                      decoration: const InputDecoration(
                        labelText: 'Série/Ano',
                        border: OutlineInputBorder(),
                      ),
                      items: List.generate(9, (index) => index + 1)
                          .map((val) => DropdownMenuItem(value: val, child: Text('$valº Ano')))
                          .toList(),
                      onChanged: (val) {
                        if (val != null) {
                          setDialogState(() {
                            selectedSeries = val;
                          });
                        }
                      },
                    ),
                  ],
                ),
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Cancelar'),
                ),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF1ABC9C), foregroundColor: Colors.white),
                  onPressed: () async {
                    if (nameController.text.trim().isEmpty) return;
                    try {
                      final repo = ref.read(classroomRepositoryProvider);
                      await repo.createClassroom(
                        nameController.text.trim(),
                        selectedLevel,
                        selectedSeries,
                      );
                      ref.invalidate(classroomsProvider);
                      if (context.mounted) {
                        Navigator.pop(context);
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Turma criada com sucesso!'), backgroundColor: Colors.green),
                        );
                      }
                    } catch (e) {
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('Erro ao criar turma: $e'), backgroundColor: Colors.red),
                        );
                      }
                    }
                  },
                  child: const Text('Criar'),
                ),
              ],
            );
          },
        );
      },
    );
  }

  void _showCreateAssignmentDialog(String classroomId) {
    final titleController = TextEditingController();
    final descController = TextEditingController();
    String selectedType = 'essay';

    showDialog(
      context: context,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setDialogState) {
            return AlertDialog(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              title: Text('Criar Nova Tarefa', style: GoogleFonts.inter(fontWeight: FontWeight.bold)),
              content: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    TextField(
                      controller: titleController,
                      decoration: const InputDecoration(
                        labelText: 'Título da Tarefa',
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: descController,
                      maxLines: 3,
                      decoration: const InputDecoration(
                        labelText: 'Descrição / Proposta',
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 16),
                    DropdownButtonFormField<String>(
                      value: selectedType,
                      decoration: const InputDecoration(
                        labelText: 'Tipo de Tarefa',
                        border: OutlineInputBorder(),
                      ),
                      items: const [
                        DropdownMenuItem(value: 'essay', child: Text('Redação (Avaliada por IA)')),
                        DropdownMenuItem(value: 'quiz', child: Text('Questionário (Múltipla Escolha)')),
                        DropdownMenuItem(value: 'exercise', child: Text('Exercício de Fixação')),
                      ],
                      onChanged: (val) {
                        if (val != null) {
                          setDialogState(() {
                            selectedType = val;
                          });
                        }
                      },
                    ),
                  ],
                ),
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Cancelar'),
                ),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF2C3E50), foregroundColor: Colors.white),
                  onPressed: () async {
                    if (titleController.text.trim().isEmpty) return;
                    try {
                      final repo = ref.read(classroomRepositoryProvider);
                      await repo.createAssignment(
                        classroomId: classroomId,
                        title: titleController.text.trim(),
                        type: selectedType,
                        description: descController.text.trim(),
                        dueDate: DateTime.now().add(const Duration(days: 7)), // Prazo padrão: 7 dias
                      );
                      ref.invalidate(classroomAssignmentsProvider(classroomId));
                      if (context.mounted) {
                        Navigator.pop(context);
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Tarefa atribuída com sucesso!'), backgroundColor: Colors.green),
                        );
                      }
                    } catch (e) {
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('Erro ao criar tarefa: $e'), backgroundColor: Colors.red),
                        );
                      }
                    }
                  },
                  child: const Text('Atribuir'),
                ),
              ],
            );
          },
        );
      },
    );
  }

  Widget _buildEssaysTab() {
    final essaysAsync = ref.watch(allEssaysProvider);

    return Scaffold(
      backgroundColor: Colors.transparent,
      body: essaysAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Erro ao carregar redações: $err')),
        data: (essays) {
          if (essays.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.rate_review_outlined, size: 64, color: Colors.grey.shade400),
                  const SizedBox(height: 16),
                  Text(
                    'Nenhuma redação enviada pelos alunos ainda.',
                    style: GoogleFonts.inter(fontSize: 16, color: Colors.grey.shade600, fontWeight: FontWeight.w500),
                  ),
                ],
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: () async {
              ref.invalidate(allEssaysProvider);
            },
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: essays.length,
              itemBuilder: (context, index) {
                final essay = essays[index];
                return _buildTeacherEssayCard(essay);
              },
            ),
          );
        },
      ),
    );
  }

  Widget _buildTeacherEssayCard(StudentEssay essay) {
    final isGraded = essay.status == 'graded';

    return Card(
      elevation: 2,
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Redação #${essay.id.substring(0, 5)} • ${essay.wordCount} palavras',
                        style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 16, color: const Color(0xFF2C3E50)),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        essay.assignmentId != null ? 'Tarefa Vinculada' : 'Treino Livre',
                        style: GoogleFonts.inter(fontSize: 12, color: Colors.grey.shade600),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: isGraded ? Colors.green.shade50 : Colors.orange.shade50,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: isGraded ? Colors.green.shade200 : Colors.orange.shade200),
                  ),
                  child: Text(
                    isGraded ? 'Avaliada por Você' : 'Correção IA (Pendente)',
                    style: GoogleFonts.inter(
                      color: isGraded ? Colors.green.shade700 : Colors.orange.shade700,
                      fontWeight: FontWeight.bold,
                      fontSize: 11,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              'Texto do Aluno:',
              style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.grey.shade700),
            ),
            const SizedBox(height: 4),
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
                style: GoogleFonts.inter(fontSize: 14, fontStyle: FontStyle.italic),
              ),
            ),
            if (essay.aiFeedback != null) ...[
              const SizedBox(height: 12),
              Row(
                children: [
                  const Icon(Icons.psychology, size: 18, color: Colors.indigo),
                  const SizedBox(width: 4),
                  Text(
                    'Análise Sugerida pela IA (Nota: ${essay.grade?.toStringAsFixed(1) ?? "N/A"}):',
                    style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.indigo),
                  ),
                ],
              ),
              const SizedBox(height: 4),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.indigo.shade50.withOpacity(0.3),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.indigo.shade100),
                ),
                child: Text(
                  essay.aiFeedback!,
                  style: GoogleFonts.inter(fontSize: 13, color: Colors.indigo.shade900),
                ),
              ),
            ],
            if (essay.teacherFeedback != null && essay.teacherFeedback!.isNotEmpty) ...[
              const SizedBox(height: 12),
              Text(
                'Sua Avaliação Atual (Nota: ${essay.grade?.toStringAsFixed(1)}):',
                style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.teal),
              ),
              const SizedBox(height: 4),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.teal.shade50.withOpacity(0.3),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.teal.shade100),
                ),
                child: Text(
                  essay.teacherFeedback!,
                  style: GoogleFonts.inter(fontSize: 13, color: Colors.teal.shade900),
                ),
              ),
            ],
            const SizedBox(height: 16),
            Align(
              alignment: Alignment.centerRight,
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF2C3E50),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                ),
                onPressed: () => _showReviewEssayDialog(essay),
                icon: const Icon(Icons.edit_note, size: 18),
                label: Text(
                  isGraded ? 'Ajustar Nota/Feedback' : 'Avaliar & Ajustar',
                  style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 13),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showReviewEssayDialog(StudentEssay essay) {
    final gradeController = TextEditingController(text: essay.grade?.toString() ?? '8.0');
    final feedbackController = TextEditingController(text: essay.teacherFeedback ?? '');

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          title: Text('Avaliação de Redação', style: GoogleFonts.inter(fontWeight: FontWeight.bold)),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Revise a redação do aluno e ajuste a nota final e observações de acordo com os critérios pedagógicos.',
                  style: GoogleFonts.inter(fontSize: 13, color: Colors.grey.shade600),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: gradeController,
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  decoration: const InputDecoration(
                    labelText: 'Nota Final (0.0 a 10.0)',
                    border: OutlineInputBorder(),
                    hintText: 'Ex: 8.5',
                  ),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: feedbackController,
                  maxLines: 4,
                  decoration: const InputDecoration(
                    labelText: 'Observações e Feedback do Professor',
                    border: OutlineInputBorder(),
                    hintText: 'Digite suas recomendações pedagógicas para o aluno...',
                  ),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancelar'),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF2C3E50), foregroundColor: Colors.white),
              onPressed: () async {
                final gradeVal = double.tryParse(gradeController.text);
                if (gradeVal == null || gradeVal < 0 || gradeVal > 10) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Por favor, insira uma nota válida entre 0 e 10!'), backgroundColor: Colors.orange),
                  );
                  return;
                }

                try {
                  final repo = ref.read(classroomRepositoryProvider);
                  await repo.updateEssayFeedback(
                    essay.id,
                    gradeVal,
                    feedbackController.text.trim(),
                  );
                  ref.invalidate(allEssaysProvider);
                  ref.invalidate(essaysProvider);
                  if (context.mounted) {
                    Navigator.pop(context);
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Avaliação salva com sucesso!'), backgroundColor: Colors.green),
                    );
                  }
                } catch (e) {
                  if (context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Erro ao salvar avaliação: $e'), backgroundColor: Colors.red),
                    );
                  }
                }
              },
              child: const Text('Salvar'),
            ),
          ],
        );
      },
    );
  }

  void _showClassroomReport(String classroomId) {
    showDialog(
      context: context,
      builder: (context) {
        return Dialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Container(
            constraints: BoxConstraints(
              maxWidth: MediaQuery.of(context).size.width * 0.85,
              maxHeight: MediaQuery.of(context).size.height * 0.8,
            ),
            padding: const EdgeInsets.all(24),
            child: Consumer(
              builder: (context, ref, child) {
                final statsAsync = ref.watch(classroomStatsProvider(classroomId));

                return statsAsync.when(
                  loading: () => const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        CircularProgressIndicator(valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF2C3E50))),
                        SizedBox(height: 16),
                        Text('Carregando estatísticas da turma...', style: TextStyle(fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
                  error: (err, stack) => Center(child: Text('Erro ao carregar estatísticas: $err')),
                  data: (stats) {
                    return SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Expanded(
                                child: Text(
                                  stats.name,
                                  style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 20, color: const Color(0xFF2C3E50)),
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                              IconButton(
                                icon: const Icon(Icons.close),
                                onPressed: () => Navigator.pop(context),
                              ),
                            ],
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Relatório de Desempenho Pedagógico',
                            style: GoogleFonts.inter(fontSize: 14, color: Colors.grey.shade600),
                          ),
                          const Divider(height: 24),
                          
                          // Cards rápidos
                          Row(
                            children: [
                              Expanded(
                                child: _buildMetricCard(
                                  icon: Icons.people,
                                  color: Colors.blue,
                                  title: 'Estudantes',
                                  value: '${stats.studentsCount}',
                                ),
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                child: _buildMetricCard(
                                  icon: Icons.grade,
                                  color: Colors.green,
                                  title: 'Média de Notas',
                                  value: _calculateAverageGrade(stats.assignmentsStats),
                                ),
                              ),
                            ],
                          ),
                          
                          const SizedBox(height: 24),
                          Text(
                            'Média de Notas por Tarefa',
                            style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 16, color: const Color(0xFF2C3E50)),
                          ),
                          const SizedBox(height: 12),
                          if (stats.assignmentsStats.isEmpty)
                            Padding(
                              padding: const EdgeInsets.symmetric(vertical: 16.0),
                              child: Text(
                                'Nenhuma tarefa de redação avaliada nesta turma ainda.',
                                style: GoogleFonts.inter(color: Colors.grey.shade500, fontStyle: FontStyle.italic, fontSize: 13),
                              ),
                            )
                          else
                            ...stats.assignmentsStats.map((stat) => _buildStatBar(
                                  title: stat.title,
                                  value: stat.averageGrade ?? 0.0,
                                  maxValue: 10.0,
                                  suffix: '/10',
                                  barColor: Colors.teal.shade400,
                                )),

                          const SizedBox(height: 24),
                          Text(
                            'Taxa de Entrega de Redações',
                            style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 16, color: const Color(0xFF2C3E50)),
                          ),
                          const SizedBox(height: 12),
                          if (stats.assignmentsStats.isEmpty)
                            Padding(
                              padding: const EdgeInsets.symmetric(vertical: 16.0),
                              child: Text(
                                'Nenhuma tarefa atribuída nesta turma ainda.',
                                style: GoogleFonts.inter(color: Colors.grey.shade500, fontStyle: FontStyle.italic, fontSize: 13),
                              ),
                            )
                          else
                            ...stats.assignmentsStats.map((stat) => _buildStatBar(
                                  title: stat.title,
                                  value: stat.submissionsPercentage,
                                  maxValue: 100.0,
                                  suffix: '%',
                                  barColor: Colors.indigo.shade300,
                                  labelInfo: '${stat.submissionsCount}/${stats.studentsCount} alunos',
                                )),
                        ],
                      ),
                    );
                  },
                );
              },
            ),
          ),
        );
      },
    );
  }

  Widget _buildMetricCard({
    required IconData icon,
    required Color color,
    required String title,
    required String value,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade200),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.02),
            blurRadius: 6,
            offset: const Offset(0, 3),
          )
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withOpacity(0.15),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, color: color, size: 20),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: GoogleFonts.inter(fontSize: 11, color: Colors.grey.shade500, fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 2),
                Text(
                  value,
                  style: GoogleFonts.inter(fontSize: 16, fontWeight: FontWeight.bold, color: const Color(0xFF2C3E50)),
                ),
              ],
            ),
          )
        ],
      ),
    );
  }

  String _calculateAverageGrade(List<AssignmentStat> stats) {
    final validGrades = stats.where((s) => s.averageGrade != null).map((s) => s.averageGrade!);
    if (validGrades.isEmpty) return 'N/A';
    final sum = validGrades.reduce((a, b) => a + b);
    return (sum / validGrades.length).toStringAsFixed(1);
  }

  Widget _buildStatBar({
    required String title,
    required double value,
    required double maxValue,
    required String suffix,
    required Color barColor,
    String? labelInfo,
  }) {
    final double percentage = maxValue > 0 ? (value / maxValue).clamp(0.0, 1.0) : 0.0;

    return Padding(
      padding: const EdgeInsets.only(bottom: 16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Text(
                  title,
                  style: GoogleFonts.inter(fontWeight: FontWeight.w600, fontSize: 13, color: Colors.grey.shade800),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              const SizedBox(width: 8),
              Text(
                '${value.toStringAsFixed(1)}$suffix',
                style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 13, color: const Color(0xFF2C3E50)),
              ),
            ],
          ),
          if (labelInfo != null) ...[
            const SizedBox(height: 2),
            Text(
              labelInfo,
              style: GoogleFonts.inter(fontSize: 11, color: Colors.grey.shade500),
            ),
          ],
          const SizedBox(height: 6),
          Stack(
            children: [
              Container(
                height: 8,
                width: double.infinity,
                decoration: BoxDecoration(
                  color: Colors.grey.shade200,
                  borderRadius: BorderRadius.circular(4),
                ),
              ),
              LayoutBuilder(
                builder: (context, constraints) {
                  return Container(
                    height: 8,
                    width: constraints.maxWidth * percentage,
                    decoration: BoxDecoration(
                      color: barColor,
                      borderRadius: BorderRadius.circular(4),
                    ),
                  );
                },
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _TeacherAssignmentsList extends ConsumerWidget {
  final String classroomId;
  const _TeacherAssignmentsList({required this.classroomId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final assignmentsAsync = ref.watch(classroomAssignmentsProvider(classroomId));

    return assignmentsAsync.when(
      loading: () => const Center(child: SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2))),
      error: (err, stack) => Text('Erro: $err', style: const TextStyle(color: Colors.red)),
      data: (assignments) {
        if (assignments.isEmpty) {
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 8.0),
            child: Text(
              'Nenhuma tarefa cadastrada nesta turma ainda.',
              style: GoogleFonts.inter(fontSize: 13, color: Colors.grey.shade500, fontStyle: FontStyle.italic),
            ),
          );
        }

        return ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: assignments.length,
          itemBuilder: (context, index) {
            final assignment = assignments[index];
            return Card(
              color: Colors.white,
              elevation: 0,
              margin: const EdgeInsets.only(bottom: 8),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8), side: BorderSide(color: Colors.grey.shade200)),
              child: ListTile(
                title: Text(assignment.title, style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 14)),
                subtitle: Text(
                  'Tipo: ${assignment.type == 'essay' ? 'Redação' : 'Questionário'} • Descrição: ${assignment.description ?? "Sem descrição"}',
                  style: GoogleFonts.inter(fontSize: 12),
                ),
                trailing: const Icon(Icons.assignment, color: Colors.blueGrey, size: 20),
              ),
            );
          },
        );
      },
    );
  }
}
