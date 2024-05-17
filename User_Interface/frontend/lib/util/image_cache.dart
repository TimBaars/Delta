import 'dart:typed_data';

class ImageCache {
  final List<Uint8List> _cache = [];

  Uint8List? get lastImage => _cache.isNotEmpty? _cache.last : null;
  Uint8List? get secondLastImage => _cache.length > 1? _cache[_cache.length - 2] : null;

  void addImage(Uint8List image) {
    if (_cache.length > 1) {
      _cache.removeAt(0);
    }
    
    _cache.add(image);
  }
}
