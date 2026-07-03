import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/dio_client.dart';
import '../../course/domain/course_models.dart';

class AdminRepository {
  Future<Topic> createTopic(String unitId, Map<String, dynamic> topicData) async {
    try {
      final response = await DioClient.instance.post(
        '/units/$unitId/topics/',
        data: topicData,
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        return Topic.fromJson(response.data);
      }
      throw Exception('Failed to create topic');
    } catch (e) {
      throw Exception('Admin API Error (Topic): $e');
    }
  }

  Future<Question> createQuestion(String topicId, Map<String, dynamic> questionData) async {
    try {
      final response = await DioClient.instance.post(
        '/topics/$topicId/questions/',
        data: questionData,
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        return Question.fromJson(response.data);
      }
      throw Exception('Failed to create question');
    } catch (e) {
      throw Exception('Admin API Error (Question): $e');
    }
  }
}

final adminRepositoryProvider = Provider<AdminRepository>((ref) {
  return AdminRepository();
});
