// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'register_screen.dart';
import 'signin_screen.dart';
import 'home_screen.dart';
import '../services/firebase_auth_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Aquí podrías poner una animación de moneda girando
              Icon(Icons.monetization_on, size: 100, color: Color(0xFFA9F00F)),
              const SizedBox(height: 20),
              const Text(
                '¿Listo para ahorrar?',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 40),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF547808),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                ),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const RegisterScreen(),
                    ),
                  );
                },
                child: const Text('Comenzar'),
              ),
              const SizedBox(height: 10),
              TextButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const SignInScreen(),
                    ),
                  );
                },
                child: const Text('Iniciar Sesión'),
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFFF0F4F1),
                  foregroundColor: const Color(0xFF111A23),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                ),
                icon: const Icon(Icons.account_circle),
                label: const Text('Continuar con Google'),
                onPressed: () async {
                  final user = await FirebaseAuthService().signInWithGoogle();

                  if (user != null) {
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const HomeScreen(),
                      ),
                    );
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('Inicio de sesión cancelado'),
                      ),
                    );
                  }
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
