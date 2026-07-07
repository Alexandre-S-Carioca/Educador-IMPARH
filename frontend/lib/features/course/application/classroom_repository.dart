import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/dio_client.dart';
import '../domain/classroom_models.dart';

class ClassroomRepository {
  // --- TURMAS (ClassRooms) ---

  Future<List<ClassRoom>> fetchClassrooms() async {
    try {
      final response = await DioClient.instance.get('/classrooms/');
      if (response.statusCode == 200) {
        final List data = response.data;
        return data.map((json) => ClassRoom.fromJson(json)).toList();
      }
      throw Exception('Falha ao carregar as turmas');
    } catch (e) {
      throw Exception('Erro de rede ao buscar turmas: $e');
    }
  }

  Future<ClassRoom> createClassroom(String name, String level, int series) async {
    try {
      final response = await DioClient.instance.post(
        '/classrooms/',
        data: {
          'name': name,
          'level': level,
          'series': series,
        },
      );
      if (response.statusCode == 200) {
        return ClassRoom.fromJson(response.data);
      }
      throw Exception('Falha ao criar turma');
    } catch (e) {
      throw Exception('Erro de rede ao criar turma: $e');
    }
  }

  Future<void> addStudentToClassroom(String classroomId, String studentId) async {
    try {
      final response = await DioClient.instance.post('/classrooms/$classroomId/students/$studentId');
      if (response.statusCode != 200) {
        throw Exception('Falha ao adicionar aluno à turma');
      }
    } catch (e) {
      throw Exception('Erro de rede ao adicionar aluno: $e');
    }
  }

  // --- TAREFAS (Assignments) ---

  Future<List<Assignment>> fetchAssignments(String classroomId) async {
    try {
      final response = await DioClient.instance.get('/assignments/classroom/$classroomId');
      if (response.statusCode == 200) {
        final List data = response.data;
        return data.map((json) => Assignment.fromJson(json)).toList();
      }
      throw Exception('Falha ao carregar as tarefas');
    } catch (e) {
      throw Exception('Erro de rede ao buscar tarefas: $e');
    }
  }

  Future<Assignment> createAssignment({
    required String classroomId,
    required String title,
    required String type,
    String? description,
    DateTime? dueDate,
  }) async {
    try {
      final response = await DioClient.instance.post(
        '/assignments/',
        data: {
          'classroom_id': classroomId,
          'title': title,
          'type': type,
          'description': description,
          'due_date': dueDate?.toIso8601String(),
        },
      );
      if (response.statusCode == 200) {
        return Assignment.fromJson(response.data);
      }
      throw Exception('Falha ao criar tarefa');
    } catch (e) {
      throw Exception('Erro de rede ao criar tarefa: $e');
    }
  }

  // --- REDAÇÕES (StudentEssays) ---

  Future<List<StudentEssay>> fetchStudentEssays({bool allEssays = false}) async {
    try {
      final response = await DioClient.instance.get(
        '/essays/',
        queryParameters: {'all_essays': allEssays},
      );
      if (response.statusCode == 200) {
        final List data = response.data;
        return data.map((json) => StudentEssay.fromJson(json)).toList();
      }
      throw Exception('Falha ao carregar redações');
    } catch (e) {
      throw Exception('Erro de rede ao buscar redações: $e');
    }
  }

  Future<StudentEssay> submitEssay(String content, {String? assignmentId}) async {
    try {
      final response = await DioClient.instance.post(
        '/essays/',
        data: {
          'content': content,
          'assignment_id': assignmentId,
        },
      );
      if (response.statusCode == 200) {
        return StudentEssay.fromJson(response.data);
      }
      throw Exception('Falha ao enviar redação');
    } catch (e) {
      throw Exception('Erro de rede ao enviar redação: $e');
    }
  }

  Future<StudentEssay> fetchEssayDetails(String essayId) async {
    try {
      final response = await DioClient.instance.get('/essays/$essayId');
      if (response.statusCode == 200) {
        return StudentEssay.fromJson(response.data);
      }
      throw Exception('Falha ao buscar detalhes da redação');
    } catch (e) {
      throw Exception('Erro de rede ao buscar detalhes: $e');
    }
  }

  Future<StudentEssay> updateEssayFeedback(String essayId, double grade, String feedback) async {
    try {
      final response = await DioClient.instance.put(
        '/essays/$essayId/feedback',
        queryParameters: {
          'grade': grade,
          'teacher_feedback': feedback,
        },
      );
      if (response.statusCode == 200) {
        return StudentEssay.fromJson(response.data);
      }
      throw Exception('Falha ao atualizar feedback da redação');
    } catch (e) {
      throw Exception('Erro de rede ao atualizar feedback: $e');
    }
  }

  Future<ClassroomStats> fetchClassroomStats(String classroomId) async {
    try {
      final response = await DioClient.instance.get('/classrooms/$classroomId/stats');
      if (response.statusCode == 200) {
        return ClassroomStats.fromJson(response.data);
      }
      throw Exception('Falha ao carregar as estatísticas da turma');
    } catch (e) {
      throw Exception('Erro de rede ao buscar estatísticas: $e');
    }
  }

  Future<List<AudioContent>> fetchTopicAudio(String topicId) async {
    try {
      final response = await DioClient.instance.get('/audio/topic/$topicId');
      if (response.statusCode == 200) {
        final List data = response.data;
        return data.map((json) => AudioContent.fromJson(json)).toList();
      }
      throw Exception('Falha ao carregar as pronúncias do tópico');
    } catch (e) {
      throw Exception('Erro de rede ao buscar pronúncias: $e');
    }
  }

  Future<Map<String, dynamic>?> fetchWikiSummary(String query) async {
    try {
      final response = await DioClient.instance.get('/wiki/summary', queryParameters: {'query': query});
      if (response.statusCode == 200) {
        return response.data;
      }
      return null;
    } catch (e) {
      return null;
    }
  }

  Future<List<YouTubeVideo>> fetchRelatedVideos(String query) async {
    try {
      final response = await DioClient.instance.get('/youtube/search', queryParameters: {'query': query});
      if (response.statusCode == 200) {
        final List data = response.data;
        return data.map((json) => YouTubeVideo.fromJson(json)).toList();
      }
      throw Exception('Falha ao buscar vídeos do YouTube');
    } catch (e) {
      throw Exception('Erro de rede ao buscar vídeos: $e');
    }
  }

  Future<List<ClassicBook>> fetchClassicBooks() async {
    try {
      final response = await DioClient.instance.get('/library/classics');
      if (response.statusCode == 200) {
        final List data = response.data;
        return data.map((json) => ClassicBook.fromJson(json)).toList();
      }
      throw Exception('Falha ao carregar livros clássicos');
    } catch (e) {
      throw Exception('Erro de rede ao buscar livros: $e');
    }
  }
}

// --- PROVIDERS RIVERPOD ---

final classroomRepositoryProvider = Provider<ClassroomRepository>((ref) {
  return ClassroomRepository();
});

final classroomsProvider = FutureProvider<List<ClassRoom>>((ref) async {
  final repo = ref.watch(classroomRepositoryProvider);
  return repo.fetchClassrooms();
});

final essaysProvider = FutureProvider<List<StudentEssay>>((ref) async {
  final repo = ref.watch(classroomRepositoryProvider);
  return repo.fetchStudentEssays();
});

final allEssaysProvider = FutureProvider<List<StudentEssay>>((ref) async {
  final repo = ref.watch(classroomRepositoryProvider);
  return repo.fetchStudentEssays(allEssays: true);
});

final classroomAssignmentsProvider = FutureProvider.family<List<Assignment>, String>((ref, classroomId) async {
  final repo = ref.watch(classroomRepositoryProvider);
  return repo.fetchAssignments(classroomId);
});

final classroomStatsProvider = FutureProvider.family<ClassroomStats, String>((ref, classroomId) async {
  final repo = ref.watch(classroomRepositoryProvider);
  return repo.fetchClassroomStats(classroomId);
});

final topicAudioProvider = FutureProvider.family<List<AudioContent>, String>((ref, topicId) async {
  final repo = ref.watch(classroomRepositoryProvider);
  return repo.fetchTopicAudio(topicId);
});

final wikiSummaryProvider = FutureProvider.family<Map<String, dynamic>?, String>((ref, query) async {
  final repo = ref.watch(classroomRepositoryProvider);
  return repo.fetchWikiSummary(query);
});

final youtubeVideosProvider = FutureProvider.family<List<YouTubeVideo>, String>((ref, query) async {
  final repo = ref.watch(classroomRepositoryProvider);
  return repo.fetchRelatedVideos(query);
});

final classicBooksProvider = FutureProvider<List<ClassicBook>>((ref) async {
  final repo = ref.watch(classroomRepositoryProvider);
  return repo.fetchClassicBooks();
});
