// =============================================
// VOCAL MASTERY ACADEMY — Module Template
// Each module includes this AFTER vma-engine.js
// Replace {MODULE} and {TOTAL} with actual values
// =============================================

(function() {
  'use strict';
  
  var MOD = {MODULE};
  var TOTAL = {TOTAL};
  var CORRECT = {ANSWERS};
  
  var s = VMA.getStudent();
  if (!s) { window.location.href = 'academy.html'; return; }
  
  var currentLesson = 1;
  
  // --- Lesson Navigation ---
  window.showLesson = function(n) {
    for (var i = 1; i <= TOTAL; i++) {
      var el = document.getElementById('lesson-' + MOD + '-' + i);
      if (el) el.style.display = (i === n) ? '' : 'none';
    }
    currentLesson = n;
    window.scrollTo({top:0, behavior:'smooth'});
    
    var st = VMA.getStudent();
    if (st) {
      st.lessons = st.lessons || {};
      st.lessons[MOD + '-' + n] = true;
      VMA.setStudent(st);
      VMA.awardXP(10, 'Lesson ' + MOD + '.' + n);
    }
    updateProgress();
  };
  
  // --- Task Completion ---
  window.completeTask = function(taskId) {
    var btn = document.getElementById('taskBtn-' + taskId);
    if (!btn) return;
    btn.textContent = '✓ Submitted';
    btn.className = 'task-btn done';
    btn.onclick = null;
    
    VMA.awardXP(25, 'Task ' + taskId);
    VMA.updateStreak();
    VMA.showNotification('✓ Task complete! +25 XP');
    
    var lessonNum = parseInt(taskId.split('-')[1]);
    if (lessonNum < TOTAL) {
      setTimeout(function() { showLesson(lessonNum + 1); }, 800);
    } else {
      setTimeout(function() { showQuiz(); }, 800);
    }
    updateProgress();
  };
  
  // --- Quiz ---
  var quizAnswers = {};
  var quizSubmitted = false;
  
  window.selectOpt = function(btn, qId) {
    if (quizSubmitted) return;
    var parent = btn.parentElement;
    var opts = parent.querySelectorAll('.q-opt');
    for (var i = 0; i < opts.length; i++) opts[i].classList.remove('selected');
    btn.classList.add('selected');
    quizAnswers[qId] = Array.from(opts).indexOf(btn);
    
    var allAnswered = true;
    for (var key in CORRECT) {
      if (quizAnswers[key] === undefined) { allAnswered = false; break; }
    }
    document.getElementById('quizSubmit').disabled = !allAnswered;
  };
  
  window.submitQuiz = function() {
    if (quizSubmitted) return;
    quizSubmitted = true;
    var correct = 0;
    var totalQ = Object.keys(CORRECT).length;
    
    for (var qId in CORRECT) {
      var correctIdx = CORRECT[qId];
      var opts = document.querySelectorAll('#' + qId + ' .q-opt');
      var selected = quizAnswers[qId];
      for (var j = 0; j < opts.length; j++) {
        if (j === correctIdx) opts[j].classList.add('correct');
        if (j === selected && j !== correctIdx) opts[j].classList.add('wrong');
      }
      if (selected === correctIdx) correct++;
    }
    
    var pct = Math.round((correct / totalQ) * 100);
    document.getElementById('quizScore').textContent = pct + '%';
    
    if (pct >= 80) {
      document.getElementById('quizTitle').textContent = '🎉 Passed!';
      document.getElementById('quizMsg').textContent = 'You scored ' + correct + '/' + totalQ + '. Great work!';
      document.getElementById('quizSubmit').style.display = 'none';
      
      VMA.awardXP(15, 'Module ' + MOD + ' Quiz (' + pct + '%)');
      var st = VMA.getStudent();
      if (st) {
        st.quizzes = st.quizzes || {};
        st.quizzes[MOD] = pct;
        st.modules[MOD - 1] = 100;
        VMA.setStudent(st);
        VMA.showNotification('🏆 Module ' + MOD + ' Complete! +15 XP');
      }
      setTimeout(function() {
        document.getElementById('quiz-' + MOD).style.display = 'none';
        document.getElementById('modComplete').style.display = '';
        document.getElementById('modComplete').scrollIntoView({behavior:'smooth', block:'center'});
      }, 2000);
    } else {
      document.getElementById('quizTitle').textContent = 'Not quite there';
      document.getElementById('quizMsg').textContent = 'You scored ' + correct + '/' + totalQ + '. You need 80% to pass. Review and try again!';
      document.getElementById('quizSubmit').style.display = 'none';
      document.getElementById('quizResult').style.display = '';
    }
  };
  
  window.retryQuiz = function() {
    quizAnswers = {};
    quizSubmitted = false;
    var opts = document.querySelectorAll('.q-opt');
    for (var i = 0; i < opts.length; i++) opts[i].classList.remove('selected','correct','wrong');
    document.getElementById('quizSubmit').disabled = true;
    document.getElementById('quizSubmit').style.display = '';
    document.getElementById('quizResult').style.display = 'none';
    document.getElementById('quizScore').textContent = '0%';
    document.getElementById('quizTitle').textContent = 'Quiz Complete';
    document.getElementById('quizMsg').textContent = 'Review the lessons and try again.';
  };
  
  window.showQuiz = function() {
    document.getElementById('quiz-' + MOD).style.display = '';
    document.getElementById('modComplete').style.display = 'none';
    window.scrollTo({top:0, behavior:'smooth'});
  };
  
  // --- Progress ---
  function updateProgress() {
    var st = VMA.getStudent();
    if (!st) return;
    var lessonsDone = 0;
    for (var i = 1; i <= TOTAL; i++) {
      if (st.lessons && st.lessons[MOD + '-' + i]) lessonsDone++;
    }
    var tasksDone = document.querySelectorAll('.task-btn.done').length;
    var quizPassed = st.quizzes && st.quizzes[MOD] >= 80;
    var pct = Math.round(((lessonsDone + tasksDone + (quizPassed ? 2 : 0)) / (TOTAL + TOTAL + 2)) * 100);
    document.getElementById('modProgress').style.width = pct + '%';
  }
  
  // --- Init ---
  var startLesson = 1;
  for (var i = 1; i <= TOTAL; i++) {
    if (!s.lessons || !s.lessons[MOD + '-' + i]) { startLesson = i; break; }
    if (i === TOTAL) startLesson = TOTAL;
  }
  
  if (s.quizzes && s.quizzes[MOD] >= 80) {
    document.getElementById('modComplete').style.display = '';
    document.getElementById('modComplete').scrollIntoView({behavior:'smooth', block:'center'});
  } else {
    showLesson(startLesson);
  }
  updateProgress();
  document.getElementById('navAvatar').textContent = (s.name || 'S').charAt(0).toUpperCase();
  
})();
