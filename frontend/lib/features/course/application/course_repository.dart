import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/dio_client.dart';
import '../domain/course_models.dart';

class CourseRepository {
  Future<List<Course>> fetchCourses() async {
    try {
      final response = await DioClient.instance.get('/courses/');
      if (response.statusCode == 200) {
        List jsonResponse = response.data;
        return jsonResponse.map((data) => Course.fromJson(data)).toList();
      }
      return [];
    } catch (e) {
      throw Exception('Failed to load courses: $e');
    }
  }

  Future<List<Module>> fetchModules(String courseId) async {
    try {
      final response = await DioClient.instance.get('/courses/$courseId/modules/');
      if (response.statusCode == 200) {
        List jsonResponse = response.data;
        return jsonResponse.map((data) => Module.fromJson(data)).toList();
      }
      return [];
    } catch (e) {
      throw Exception('Failed to load modules: $e');
    }
  }

  Future<Topic> fetchTopicDetail(String topicId) async {
    try {
      final response = await DioClient.instance.get('/topics/$topicId');
      if (response.statusCode == 200) {
        return Topic.fromJson(response.data);
      }
      throw Exception('Failed to load topic detail');
    } catch (e) {
      throw Exception('Network Error: $e');
    }
  }

  Future<List<Flashcard>> fetchTopicFlashcards(String topicId) async {
    try {
      final response = await DioClient.instance.get('/topics/$topicId/flashcards/');
      if (response.statusCode == 200) {
        final List data = response.data;
        return data.map((json) => Flashcard.fromJson(json)).toList();
      }
      throw Exception('Failed to load flashcards');
    } catch (e) {
      throw Exception('Network Error: $e');
    }
  }
}

final courseRepositoryProvider = Provider<CourseRepository>((ref) {
  return CourseRepository();
});

final coursesProvider = FutureProvider<List<Course>>((ref) async {
  final repo = ref.watch(courseRepositoryProvider);
  return repo.fetchCourses();
});

final modulesProvider = FutureProvider.family<List<Module>, String>((ref, courseId) async {
  final repo = ref.watch(courseRepositoryProvider);
  return repo.fetchModules(courseId);
});

final topicDetailProvider = FutureProvider.family<Topic, String>((ref, topicId) async {
  final repo = ref.watch(courseRepositoryProvider);
  return repo.fetchTopicDetail(topicId);
});

final topicFlashcardsProvider = FutureProvider.family<List<Flashcard>, String>((ref, topicId) async {
  final repo = ref.watch(courseRepositoryProvider);
  return repo.fetchTopicFlashcards(topicId);
});
