class Question {
  final String id;
  final String statement;
  final String optionA;
  final String optionB;
  final String optionC;
  final String optionD;
  final String correctOption;
  final String justificationCorrect;
  final String justificationIncorrect;

  Question({
    required this.id,
    required this.statement,
    required this.optionA,
    required this.optionB,
    required this.optionC,
    required this.optionD,
    required this.correctOption,
    required this.justificationCorrect,
    required this.justificationIncorrect,
  });

  factory Question.fromJson(Map<String, dynamic> json) {
    return Question(
      id: json['id'],
      statement: json['statement'],
      optionA: json['option_a'],
      optionB: json['option_b'],
      optionC: json['option_c'],
      optionD: json['option_d'],
      correctOption: json['correct_option'],
      justificationCorrect: json['justification_correct'],
      justificationIncorrect: json['justification_incorrect'],
    );
  }
}

class Flashcard {
  final String id;
  final String topicId;
  final String front;
  final String back;

  Flashcard({
    required this.id,
    required this.topicId,
    required this.front,
    required this.back,
  });

  factory Flashcard.fromJson(Map<String, dynamic> json) {
    return Flashcard(
      id: json['id'],
      topicId: json['topic_id'],
      front: json['front'],
      back: json['back'],
    );
  }
}

class Topic {
  final String id;
  final String title;
  final String? introduction;
  final String? theoryMarkdown;
  final List<Question> questions;

  Topic({
    required this.id,
    required this.title,
    this.introduction,
    this.theoryMarkdown,
    this.questions = const [],
  });

  factory Topic.fromJson(Map<String, dynamic> json) {
    var list = json['questions'] as List? ?? [];
    List<Question> questionList = list.map((i) => Question.fromJson(i)).toList();

    return Topic(
      id: json['id'],
      title: json['title'],
      introduction: json['introduction'],
      theoryMarkdown: json['theory_markdown'],
      questions: questionList,
    );
  }
}

class Unit {
  final String id;
  final String title;
  final List<Topic> topics;

  Unit({required this.id, required this.title, this.topics = const []});

  factory Unit.fromJson(Map<String, dynamic> json) {
    var list = json['topics'] as List? ?? [];
    List<Topic> topicList = list.map((i) => Topic.fromJson(i)).toList();
    return Unit(
      id: json['id'],
      title: json['title'],
      topics: topicList,
    );
  }
}

class Module {
  final String id;
  final String title;
  final List<Unit> units;

  Module({required this.id, required this.title, this.units = const []});

  factory Module.fromJson(Map<String, dynamic> json) {
    var list = json['units'] as List? ?? [];
    List<Unit> unitList = list.map((i) => Unit.fromJson(i)).toList();
    return Module(
      id: json['id'],
      title: json['title'],
      units: unitList,
    );
  }
}

class Course {
  final String id;
  final String name;

  Course({required this.id, required this.name});

  factory Course.fromJson(Map<String, dynamic> json) {
    return Course(
      id: json['id'],
      name: json['name'],
    );
  }
}
