// ignore_for_file: use_build_context_synchronously

import 'package:app_gastos/pages/login_screen.dart';
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../services/firebase_auth_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int counter = 0;

  // Obtener el usuario actual
  final User? _user = FirebaseAuth.instance.currentUser;

  void incrementCounter() {
    setState(() {
      counter++;
    });
  }

  void _signOut() async {
    await FirebaseAuthService().signOut();
    // Redirigir al login después de cerrar sesión
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => const LoginScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Inicio - Finanzas Personales'),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: <Widget>[
            // Header con la foto y los datos del usuario
            UserAccountsDrawerHeader(
              accountName: Text(_user?.displayName ?? 'Usuario'),
              accountEmail: Text(_user?.email ?? 'Correo no disponible'),
              currentAccountPicture: CircleAvatar(
                backgroundImage: NetworkImage(_user?.photoURL ??
                    'https://www.example.com/default-avatar.png'),
              ),
            ),
            // Opciones del menú
            ListTile(
              leading: const Icon(Icons.home),
              title: const Text('Inicio'),
              onTap: () {
                Navigator.pop(context); // Cierra el Drawer
              },
            ),
            ListTile(
              leading: const Icon(Icons.settings),
              title: const Text('Configuración'),
              onTap: () {
                Navigator.pop(context); // Cierra el Drawer
                // Aquí puedes agregar navegación a la pantalla de configuración
              },
            ),
            ListTile(
              leading: const Icon(Icons.exit_to_app),
              title: const Text('Cerrar sesión'),
              onTap: _signOut,
            ),
          ],
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Has presionado el botón tantas veces:'),
            Text(
              '$counter',
              style: const TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: const Color(0xFFA9F00F),
        onPressed: incrementCounter,
        child: const Icon(Icons.add),
      ),
    );
  }
}
