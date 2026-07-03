import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/dio_client.dart';
import '../domain/progress_models.dart';

class ProgressRepository {
  Future<ProgressSummary> fetchSummary() async {
    try {
      final response = await DioClient.instance.get('/progress/summary');
      if (response.statusCode == 200) {
        return ProgressSummary.fromJson(response.data);
      }
      throw Exception('Failed to load summary');
    } catch (e) {
      throw Exception('Network Error: $e');
    }
  }

  Future<UserStatisticsSummary> fetchUserStatistics() async {
    try {
      final response = await DioClient.instance.get('/progress/stats');
      if (response.statusCode == 200) {
        return UserStatisticsSummary.fromJson(response.data);
      }
      throw Exception('Failed to load statistics');
    } catch (e) {
      throw Exception('Network Error: $e');
    }
  }

  Future<AttemptResponse> recordAttempt(String questionId, bool isCorrect) async {
    try {
      final response = await DioClient.instance.post(
        '/progress/attempt',
        data: {
          'question_id': questionId,
          'is_correct': isCorrect,
        },
      );
      if (response.statusCode == 200) {
        return AttemptResponse.fromJson(response.data);
      }
      throw Exception('Failed to record attempt');
    } catch (e) {
      throw Exception('Failed to record attempt: $e');
    }
  }
}

final progressRepositoryProvider = Provider<ProgressRepository>((ref) {
  return ProgressRepository();
});

final progressSummaryProvider = FutureProvider<ProgressSummary>((ref) async {
  final repo = ref.watch(progressRepositoryProvider);
  return repo.fetchSummary();
});

final userStatisticsProvider = FutureProvider<UserStatisticsSummary>((ref) async {
  final repo = ref.watch(progressRepositoryProvider);
  return repo.fetchUserStatistics();
});
