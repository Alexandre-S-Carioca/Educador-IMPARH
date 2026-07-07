class ClassRoom {
  final String id;
  final String teacherId;
  final String name;
  final String level; // fundamental_i, fundamental_ii, high_school
  final int series;
  final DateTime createdAt;
  final DateTime updatedAt;

  ClassRoom({
    required this.id,
    required this.teacherId,
    required this.name,
    required this.level,
    required this.series,
    required this.createdAt,
    required this.updatedAt,
  });

  factory ClassRoom.fromJson(Map<String, dynamic> json) {
    return ClassRoom(
      id: json['id'],
      teacherId: json['teacher_id'],
      name: json['name'],
      level: json['level'],
      series: json['series'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'teacher_id': teacherId,
      'name': name,
      'level': level,
      'series': series,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

class Assignment {
  final String id;
  final String teacherId;
  final String classroomId;
  final String title;
  final String type; // essay, quiz, exercise
  final String? description;
  final DateTime? dueDate;
  final Map<String, dynamic>? rubric;
  final DateTime createdAt;
  final DateTime updatedAt;

  Assignment({
    required this.id,
    required this.teacherId,
    required this.classroomId,
    required this.title,
    required this.type,
    this.description,
    this.dueDate,
    this.rubric,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Assignment.fromJson(Map<String, dynamic> json) {
    return Assignment(
      id: json['id'],
      teacherId: json['teacher_id'],
      classroomId: json['classroom_id'],
      title: json['title'],
      type: json['type'],
      description: json['description'],
      dueDate: json['due_date'] != null ? DateTime.parse(json['due_date']) : null,
      rubric: json['rubric'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'teacher_id': teacherId,
      'classroom_id': classroomId,
      'title': title,
      'type': type,
      'description': description,
      'due_date': dueDate?.toIso8601String(),
      'rubric': rubric,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

class StudentEssay {
  final String id;
  final String studentId;
  final String? assignmentId;
  final String content;
  final int wordCount;
  final double? grade;
  final String? aiFeedback;
  final String? teacherFeedback;
  final String status; // draft, submitted, reviewed, graded
  final DateTime createdAt;
  final DateTime updatedAt;

  StudentEssay({
    required this.id,
    required this.studentId,
    this.assignmentId,
    required this.content,
    required this.wordCount,
    this.grade,
    this.aiFeedback,
    this.teacherFeedback,
    required this.status,
    required this.createdAt,
    required this.updatedAt,
  });

  factory StudentEssay.fromJson(Map<String, dynamic> json) {
    return StudentEssay(
      id: json['id'],
      studentId: json['student_id'],
      assignmentId: json['assignment_id'],
      content: json['content'],
      wordCount: json['word_count'],
      grade: json['grade'] != null ? (json['grade'] as num).toDouble() : null,
      aiFeedback: json['ai_feedback'],
      teacherFeedback: json['teacher_feedback'],
      status: json['status'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'student_id': studentId,
      'assignment_id': assignmentId,
      'content': content,
      'word_count': wordCount,
      'grade': grade,
      'ai_feedback': aiFeedback,
      'teacher_feedback': teacherFeedback,
      'status': status,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

class StudentSubmission {
  final String id;
  final String assignmentId;
  final String studentId;
  final String? content;
  final DateTime? submittedAt;
  final double? grade;
  final String? feedback;
  final DateTime createdAt;
  final DateTime updatedAt;

  StudentSubmission({
    required this.id,
    required this.assignmentId,
    required this.studentId,
    this.content,
    this.submittedAt,
    this.grade,
    this.feedback,
    required this.createdAt,
    required this.updatedAt,
  });

  factory StudentSubmission.fromJson(Map<String, dynamic> json) {
    return StudentSubmission(
      id: json['id'],
      assignmentId: json['assignment_id'],
      studentId: json['student_id'],
      content: json['content'],
      submittedAt: json['submitted_at'] != null ? DateTime.parse(json['submitted_at']) : null,
      grade: json['grade'] != null ? (json['grade'] as num).toDouble() : null,
      feedback: json['feedback'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'assignment_id': assignmentId,
      'student_id': studentId,
      'content': content,
      'submitted_at': submittedAt?.toIso8601String(),
      'grade': grade,
      'feedback': feedback,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

class AssignmentStat {
  final String assignmentId;
  final String title;
  final int submissionsCount;
  final double submissionsPercentage;
  final double? averageGrade;

  AssignmentStat({
    required this.assignmentId,
    required this.title,
    required this.submissionsCount,
    required this.submissionsPercentage,
    this.averageGrade,
  });

  factory AssignmentStat.fromJson(Map<String, dynamic> json) {
    return AssignmentStat(
      assignmentId: json['assignment_id'],
      title: json['title'],
      submissionsCount: json['submissions_count'],
      submissionsPercentage: (json['submissions_percentage'] as num).toDouble(),
      averageGrade: json['average_grade'] != null ? (json['average_grade'] as num).toDouble() : null,
    );
  }
}

class ClassroomStats {
  final String classroomId;
  final String name;
  final int studentsCount;
  final List<AssignmentStat> assignmentsStats;

  ClassroomStats({
    required this.classroomId,
    required this.name,
    required this.studentsCount,
    required this.assignmentsStats,
  });

  factory ClassroomStats.fromJson(Map<String, dynamic> json) {
    var list = json['assignments_stats'] as List? ?? [];
    List<AssignmentStat> statsList = list.map((i) => AssignmentStat.fromJson(i)).toList();

    return ClassroomStats(
      classroomId: json['classroom_id'],
      name: json['name'],
      studentsCount: json['students_count'],
      assignmentsStats: statsList,
    );
  }
}

class AudioContent {
  final String id;
  final String topicId;
  final String wordOrPhrase;
  final String? audioUrl;
  final String? ipaPhonetic;
  final String? languageLevel;

  AudioContent({
    required this.id,
    required this.topicId,
    required this.wordOrPhrase,
    this.audioUrl,
    this.ipaPhonetic,
    this.languageLevel,
  });

  factory AudioContent.fromJson(Map<String, dynamic> json) {
    return AudioContent(
      id: json['id'],
      topicId: json['topic_id'],
      wordOrPhrase: json['word_or_phrase'],
      audioUrl: json['audio_url'],
      ipaPhonetic: json['ipa_phonetic'],
      languageLevel: json['language_level'],
    );
  }
}

class YouTubeVideo {
  final String id;
  final String title;
  final String thumbnail;
  final String videoUrl;

  YouTubeVideo({
    required this.id,
    required this.title,
    required this.thumbnail,
    required this.videoUrl,
  });

  factory YouTubeVideo.fromJson(Map<String, dynamic> json) {
    return YouTubeVideo(
      id: json['id'],
      title: json['title'],
      thumbnail: json['thumbnail'],
      videoUrl: json['video_url'],
    );
  }
}

class ClassicBook {
  final String id;
  final String title;
  final String author;
  final int year;
  final String description;
  final String downloadUrl;
  final String coverColor;

  ClassicBook({
    required this.id,
    required this.title,
    required this.author,
    required this.year,
    required this.description,
    required this.downloadUrl,
    required this.coverColor,
  });

  factory ClassicBook.fromJson(Map<String, dynamic> json) {
    return ClassicBook(
      id: json['id'],
      title: json['title'],
      author: json['author'],
      year: json['year'],
      description: json['description'],
      downloadUrl: json['download_url'],
      coverColor: json['cover_color'],
    );
  }
}
