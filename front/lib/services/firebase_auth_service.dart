import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';
import './mail_reader_service.dart';
import '../clases/gastos.dart';

class FirebaseAuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: ['https://www.googleapis.com/auth/gmail.readonly'],
  );

  Future<(User?, List<Gastos>)> signInWithGoogle() async {
    final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
    if (googleUser == null) return (null, <Gastos>[]); // Canceló

    final GoogleSignInAuthentication googleAuth =
        await googleUser.authentication;
    final credential = GoogleAuthProvider.credential(
      accessToken: googleAuth.accessToken,
      idToken: googleAuth.idToken,
    );

    final MailReaderService mailReaderService = MailReaderService();
    final List<Gastos> gastos = await mailReaderService.sendGoogleAccessToken(
      googleAuth.accessToken!,
    );

    final userCredential = await _auth.signInWithCredential(credential);
    return (userCredential.user, gastos);
  }

  Future<void> signOut() async {
    await _googleSignIn.signOut();
    await _auth.signOut();
  }

  User? get currentUser => _auth.currentUser;
}
