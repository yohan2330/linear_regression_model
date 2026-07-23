import 'package:flutter/material.dart';
import '../constants/dropdown_options.dart';
import '../services/prediction_service.dart';

class PredictionPage extends StatefulWidget {
  const PredictionPage({super.key});

  @override
  State<PredictionPage> createState() => _PredictionPageState();
}

class _PredictionPageState extends State<PredictionPage> {
  final _formKey = GlobalKey<FormState>();

  final TextEditingController _yearController = TextEditingController();
  final TextEditingController _monthController = TextEditingController();
  final TextEditingController _femaleRatioController = TextEditingController();

  String? _selectedState;
  String? _selectedGrade;
  String? _selectedReason;

  bool _isLoading = false;
  String? _resultText;
  bool _isError = false;

  @override
  void dispose() {
    _yearController.dispose();
    _monthController.dispose();
    _femaleRatioController.dispose();
    super.dispose();
  }

  Future<void> _submitPrediction() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
      _resultText = null;
      _isError = false;
    });

    try {
      final predicted = await PredictionService.predictDropoutCount(
        state: _selectedState!,
        grade: _selectedGrade!,
        year: int.parse(_yearController.text.trim()),
        month: int.parse(_monthController.text.trim()),
        femaleRatio: double.parse(_femaleRatioController.text.trim()),
        dominantReason: _selectedReason!,
      );
      setState(() {
        _resultText = "Predicted dropout count: ${predicted.toStringAsFixed(2)}";
        _isError = false;
      });
    } catch (e) {
      setState(() {
        _resultText = "$e";
        _isError = true;
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  String? _yearValidator(String? value) {
    if (value == null || value.trim().isEmpty) return 'Required';
    final n = int.tryParse(value.trim());
    if (n == null) return 'Must be a whole number';
    if (n < 2022 || n > 2027) return 'Must be between 2022 and 2027';
    return null;
  }

  String? _monthValidator(String? value) {
    if (value == null || value.trim().isEmpty) return 'Required';
    final n = int.tryParse(value.trim());
    if (n == null) return 'Must be a whole number';
    if (n < 1 || n > 12) return 'Must be between 1 and 12';
    return null;
  }

  String? _femaleRatioValidator(String? value) {
    if (value == null || value.trim().isEmpty) return 'Required';
    final n = double.tryParse(value.trim());
    if (n == null) return 'Must be a decimal number';
    if (n < 0.0 || n > 1.0) return 'Must be between 0.0 and 1.0';
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Nigerian Education Dropout Predictor'),
        centerTitle: true,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Text(
                  'Enter the details below to predict the number of '
                  'student dropouts for a given State, grade and period.',
                  style: TextStyle(fontSize: 14, color: Colors.black54),
                ),
                const SizedBox(height: 20),
                DropdownButtonFormField<String>(
                  value: _selectedState,
                  decoration: const InputDecoration(
                    labelText: 'State',
                    border: OutlineInputBorder(),
                  ),
                  isExpanded: true,
                  items: validStates
                      .map((s) => DropdownMenuItem(value: s, child: Text(s)))
                      .toList(),
                  onChanged: (value) => setState(() => _selectedState = value),
                  validator: (value) => value == null ? 'Required' : null,
                ),
                const SizedBox(height: 14),
                DropdownButtonFormField<String>(
                  value: _selectedGrade,
                  decoration: const InputDecoration(
                    labelText: 'Grade',
                    border: OutlineInputBorder(),
                  ),
                  isExpanded: true,
                  items: validGrades
                      .map((g) => DropdownMenuItem(value: g, child: Text(g)))
                      .toList(),
                  onChanged: (value) => setState(() => _selectedGrade = value),
                  validator: (value) => value == null ? 'Required' : null,
                ),
                const SizedBox(height: 14),
                TextFormField(
                  controller: _yearController,
                  keyboardType: TextInputType.number,
                  decoration: const InputDecoration(
                    labelText: 'Year (2022-2027)',
                    border: OutlineInputBorder(),
                  ),
                  validator: _yearValidator,
                ),
                const SizedBox(height: 14),
                TextFormField(
                  controller: _monthController,
                  keyboardType: TextInputType.number,
                  decoration: const InputDecoration(
                    labelText: 'Month (1-12)',
                    border: OutlineInputBorder(),
                  ),
                  validator: _monthValidator,
                ),
                const SizedBox(height: 14),
                TextFormField(
                  controller: _femaleRatioController,
                  keyboardType:
                      const TextInputType.numberWithOptions(decimal: true),
                  decoration: const InputDecoration(
                    labelText: 'Female ratio (0.0-1.0)',
                    border: OutlineInputBorder(),
                  ),
                  validator: _femaleRatioValidator,
                ),
                const SizedBox(height: 14),
                DropdownButtonFormField<String>(
                  value: _selectedReason,
                  decoration: const InputDecoration(
                    labelText: 'Dominant reason',
                    border: OutlineInputBorder(),
                  ),
                  isExpanded: true,
                  items: validReasons
                      .map((r) => DropdownMenuItem(value: r, child: Text(r)))
                      .toList(),
                  onChanged: (value) => setState(() => _selectedReason = value),
                  validator: (value) => value == null ? 'Required' : null,
                ),
                const SizedBox(height: 24),
                ElevatedButton(
                  onPressed: _isLoading ? null : _submitPrediction,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: _isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('Predict', style: TextStyle(fontSize: 16)),
                ),
                const SizedBox(height: 20),
                if (_resultText != null)
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: _isError ? Colors.red.shade50 : Colors.green.shade50,
                      border: Border.all(
                        color: _isError ? Colors.red : Colors.green,
                      ),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      _resultText!,
                      style: TextStyle(
                        color: _isError ? Colors.red.shade900 : Colors.green.shade900,
                        fontSize: 15,
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}