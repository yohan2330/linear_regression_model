import 'dart:convert';
import 'package:http/http.dart' as http;

class PredictionService {
  static const String apiUrl =
      'https://linear-regression-model-6sm2.onrender.com/predict';

  /// Calls the API and returns the predicted dropout count.
  /// Throws an [Exception] with a readable message on failure.
  static Future<double> predictDropoutCount({
    required String state,
    required String grade,
    required int year,
    required int month,
    required double femaleRatio,
    required String dominantReason,
  }) async {
    final Map<String, dynamic> requestBody = {
      "state": state,
      "grade": grade,
      "year": year,
      "month": month,
      "female_ratio": femaleRatio,
      "dominant_reason": dominantReason,
    };

    final response = await http.post(
      Uri.parse(apiUrl),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(requestBody),
    );

    final data = jsonDecode(response.body);

    if (response.statusCode == 200) {
      return (data['predicted_dropout_count'] as num).toDouble();
    } else {
      throw Exception(
          "Error (${response.statusCode}): ${data['detail'] ?? response.body}");
    }
  }
}