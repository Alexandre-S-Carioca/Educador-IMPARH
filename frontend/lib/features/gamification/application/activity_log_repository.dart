import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/dio_client.dart';
import '../domain/activity_log_models.dart';

class ActivityLogRepository {
  Future<List<ActivityLog>> fetchActivityLogs() async {
    try {
      final response = await DioClient.instance.get('/activity-logs/');
      if (response.statusCode == 200) {
        final List data = response.data;
        return data.map((json) => ActivityLog.fromJson(json)).toList();
      }
      throw Exception('Failed to load activity logs');
    } catch (e) {
      throw Exception('Network Error: $e');
    }
  }

  Future<ActivityLog> recordActivityLog(String action, String details) async {
    try {
      final response = await DioClient.instance.post(
        '/activity-logs/',
        data: {
          'action': action,
          'details': details,
        },
      );
      if (response.statusCode == 200) {
        return ActivityLog.fromJson(response.data);
      }
      throw Exception('Failed to record activity log');
    } catch (e) {
      throw Exception('Network Error: $e');
    }
  }
}

final activityLogRepositoryProvider = Provider<ActivityLogRepository>((ref) {
  return ActivityLogRepository();
});

final activityLogsProvider = FutureProvider<List<ActivityLog>>((ref) async {
  final repo = ref.watch(activityLogRepositoryProvider);
  return repo.fetchActivityLogs();
});
