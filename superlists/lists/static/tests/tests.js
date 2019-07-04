QUnit.test('smoke test', function (assert){
  assert.equal($('.has-error').is(':visible'), true, 'visible');
  $('.has-error').hide();
  assert.equal($('.has-error').is('visible'), false, 'hidden');
});
