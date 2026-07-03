class ProgressSummary {
  final String userId;
  final int totalXp;
  final int level;

  ProgressSummary({
    required this.userId,
    required this.totalXp,
    required this.level,
  });

  factory ProgressSummary.fromJson(Map<String, dynamic> json) {
    return ProgressSummary(
      userId: json['user_id'],
      totalXp: json['total_xp'],
      level: json['level'],
    );
  }
}

class UserStatisticsSummary {
  final int totalQuestions;
  final int totalCorrect;
  final int totalIncorrect;
  final double accuracyPercentage;

  UserStatisticsSummary({
    required this.totalQuestions,
    required this.totalCorrect,
    required this.totalIncorrect,
    required this.accuracyPercentage,
  });

  factory UserStatisticsSummary.fromJson(Map<String, dynamic> json) {
    return UserStatisticsSummary(
      totalQuestions: json['total_questions'],
      totalCorrect: json['total_correct'],
      totalIncorrect: json['total_incorrect'],
      accuracyPercentage: json['accuracy_percentage'].toDouble(),
    );
  }
}

class AttemptResponse {
  final String id;
  final int xpAwarded;
  final bool isCorrect;

  AttemptResponse({
    required this.id,
    required this.xpAwarded,
    required this.isCorrect,
  });

  factory AttemptResponse.fromJson(Map<String, dynamic> json) {
    return AttemptResponse(
      id: json['id'],
      xpAwarded: json['xp_awarded'],
      isCorrect: json['is_correct'],
    );
  }
}
