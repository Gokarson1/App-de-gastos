import 'package:flutter/material.dart';
import 'auth_service.dart';

class LoginPage extends StatelessWidget {
  final authService = AuthService();

  LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ElevatedButton.icon(
          icon: Icon(Icons.login),
          label: Text("Iniciar con Google"),
          onPressed: () async {
            final user = await authService.signInWithGoogle();
            if (user != null) {
              Navigator.pushReplacementNamed(context, '/home');
            }
          },
        ),
      ),
    );
  }
}
