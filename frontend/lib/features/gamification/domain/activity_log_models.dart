class ActivityLog {
  final String id;
  final String userId;
  final String action;
  final String? details;
  final DateTime createdAt;

  ActivityLog({
    required this.id,
    required this.userId,
    required this.action,
    this.details,
    required this.createdAt,
  });

  factory ActivityLog.fromJson(Map<String, dynamic> json) {
    return ActivityLog(
      id: json['id'],
      userId: json['user_id'],
      action: json['action'],
      details: json['details'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
