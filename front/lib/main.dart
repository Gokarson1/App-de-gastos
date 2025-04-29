import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main() {
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
