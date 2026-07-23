import 'package:flutter/material.dart';
import 'pages/prediction_page.dart';

void main() {
  runApp(const DropoutPredictionApp());
}

class DropoutPredictionApp extends StatelessWidget {
  const DropoutPredictionApp({super.key});

  @override
  Widget build(BuildContext context) {
    const Color aluBlue = Color(0xFF003B73);

    return MaterialApp(
      title: 'Dropout Predictor',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: Colors.white,
        colorScheme: ColorScheme.fromSeed(
          seedColor: aluBlue,
          primary: aluBlue,
          onPrimary: Colors.white,
          surface: Colors.white,
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: aluBlue,
          foregroundColor: Colors.white,
          elevation: 0,
          centerTitle: true,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: aluBlue,
            foregroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(vertical: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: const BorderSide(color: aluBlue, width: 1),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: const BorderSide(color: aluBlue, width: 2),
          ),
          labelStyle: const TextStyle(color: aluBlue),
        ),
      ),
      home: const PredictionPage(),
    );
  }
}