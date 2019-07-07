// QUnit.test('smoke test', function (assert){
//   assert.equal($('.has-error').is(':visible'), true, 'visible');
//   $('.has-error').hide();
//   assert.equal($('.has-error').is('visible'), false, 'hidden');
// });

var initialize = function () {
  $('input[name="text"]').on('keypress', function(){
    $('.has-error').hide();});
};

QUnit.test('errors are not hidden if there is no keypress', function(assert){
  assert.equal($('.has-error').is(':visible'), true);
});

QUnit.test('errors should be hidden on keypress', function (assert){
  $('input[name="text"]').trigger('keypress');
  assert.equal($('.has-error').is(':visible'), false);
});
