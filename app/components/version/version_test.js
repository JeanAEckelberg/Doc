'use strict';

describe('doc.version module', function() {
  beforeEach(module('doc.version'));

  describe('version service', function() {
    it('should return current version', inject(function(version) {
      expect(version).toEqual('0.1');
    }));
  });
});
