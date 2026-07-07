import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'features/auth/presentation/login_screen.dart';
import 'features/course/presentation/home_screen.dart';
import 'features/course/presentation/topic_screen.dart';
import 'features/course/presentation/quiz_screen.dart';
import 'features/course/presentation/flashcard_screen.dart';
import 'features/auth/application/auth_controller.dart';
import 'features/admin/presentation/admin_home_screen.dart';
import 'features/admin/presentation/admin_topic_form_screen.dart';
import 'features/admin/presentation/admin_question_form_screen.dart';
import 'features/gamification/presentation/main_navigation_screen.dart';
import 'features/course/presentation/student_assignments_screen.dart';
import 'features/course/presentation/teacher_classrooms_screen.dart';

void main() {
  runApp(
    const ProviderScope(
      child: EducadorApp(),
    ),
  );
}

final routerProvider = Provider<GoRouter>((ref) {
  final isAuthenticated = ref.watch(authProvider);

  return GoRouter(
    initialLocation: '/login',
    redirect: (context, state) {
      final isLoggingIn = state.matchedLocation == '/login';
      
      if (!isAuthenticated && !isLoggingIn) return '/login';
      if (isAuthenticated && isLoggingIn) return '/';
      
      return null;
    },
    routes: [
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/',
        builder: (context, state) => const MainNavigationScreen(),
      ),
      GoRoute(
        path: '/topic/:id',
        builder: (context, state) => TopicScreen(topicId: state.pathParameters['id']!),
      ),
      GoRoute(
        path: '/topic/:id/quiz',
        builder: (context, state) => QuizScreen(topicId: state.pathParameters['id']!),
      ),
      GoRoute(
        path: '/topic/:id/flashcards',
        builder: (context, state) => FlashcardScreen(topicId: state.pathParameters['id']!),
      ),
      GoRoute(
        path: '/admin',
        builder: (context, state) => const AdminHomeScreen(),
      ),
      GoRoute(
        path: '/admin/unit/:id/create-topic',
        builder: (context, state) => AdminTopicFormScreen(unitId: state.pathParameters['id']!),
      ),
      GoRoute(
        path: '/admin/topic/:id/create-question',
        builder: (context, state) => AdminQuestionFormScreen(topicId: state.pathParameters['id']!),
      ),
      GoRoute(
        path: '/student/assignments',
        builder: (context, state) => const StudentAssignmentsScreen(),
      ),
      GoRoute(
        path: '/student/essay/write',
        builder: (context, state) => StudentWriteEssayScreen(
          assignmentId: state.uri.queryParameters['assignmentId'],
        ),
      ),
      GoRoute(
        path: '/teacher/classrooms',
        builder: (context, state) => const TeacherClassroomsScreen(),
      ),
    ],
  );
});

class EducadorApp extends ConsumerWidget {
  const EducadorApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);

    return MaterialApp.router(
      title: 'Educador',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF203A43)),
        useMaterial3: true,
      ),
      routerConfig: router,
    );
  }
}
