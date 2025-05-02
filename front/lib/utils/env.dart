abstract class EnvConfig {
  static String baseurl = const String.fromEnvironment(
    'BACKEND_URL',
    defaultValue: 'http://localhost:8000',
  );
}
