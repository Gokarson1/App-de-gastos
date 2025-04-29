import 'package:flutter/material.dart';
import 'pages/login_screen.dart';
import 'package:firebase_core/firebase_core.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(const FinanzasPersonalesApp());
}

class FinanzasPersonalesApp extends StatelessWidget {
  const FinanzasPersonalesApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Finanzas Personales',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF111a23), // fondo oscuro
        textTheme: const TextTheme(
          bodyLarge: TextStyle(color: Colors.white),
          bodyMedium: TextStyle(color: Colors.white),
        ),
      ),
      home: const LoginScreen(),
    );
  }
}
