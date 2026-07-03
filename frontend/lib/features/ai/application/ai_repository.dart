import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/dio_client.dart';

class AiExplainResponse {
  final String explanationMarkdown;

  AiExplainResponse({required this.explanationMarkdown});

  factory AiExplainResponse.fromJson(Map<String, dynamic> json) {
    return AiExplainResponse(
      explanationMarkdown: json['explanation_markdown'],
    );
  }
}

class AiRepository {
  Future<AiExplainResponse> explainQuestion(String questionId, String selectedOption) async {
    try {
      final response = await DioClient.instance.post(
        '/ai/explain',
        data: {
          'question_id': questionId,
          'selected_option': selectedOption,
        },
      );
      if (response.statusCode == 200) {
        return AiExplainResponse.fromJson(response.data);
      }
      throw Exception('Failed to get AI explanation');
    } catch (e) {
      throw Exception('AI Tutor Error: $e');
    }
  }
}

final aiRepositoryProvider = Provider<AiRepository>((ref) {
  return AiRepository();
});
