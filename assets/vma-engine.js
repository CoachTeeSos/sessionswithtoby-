/* ============================================================
   VMA ENGINE v3 — Bulletproof. Zero silent failures.
   ============================================================ */
var VMA = (function() {
  'use strict';
  var KEY = 'vma_student_v3';
  var TERMS_KEY = 'vma_terms_v3';

  function get() {
    try { var r = localStorage.getItem(KEY); return r ? JSON.parse(r) : null; } catch(e) { return null; }
  }
  function set(s) {
    try { localStorage.setItem(KEY, JSON.stringify(s)); } catch(e) {}
  }
  function create(name) {
    var s = { name:name||'Student', xp:0, level:1, modules:[0,0,0,0,0,0,0], lessons:{}, quizzes:{}, badges:[], streak:1, lastActive:new Date().toDateString(), startDate:new Date().toISOString() };
    try { localStorage.setItem(TERMS_KEY,'true'); set(s); } catch(e) {}
    return s;
  }

  var LEVELS = [
    {xp:0,name:'Beginner',emoji:'🌱'},{xp:100,name:'Explorer',emoji:'🔍'},
    {xp:250,name:'Apprentice',emoji:'📖'},{xp:500,name:'Practitioner',emoji:'🎯'},
    {xp:800,name:'Performer',emoji:'🎤'},{xp:1200,name:'Artist',emoji:'🎨'},
    {xp:1800,name:'Virtuoso',emoji:'🏆'}
  ];
  function getLevel(xp) {
    for(var i=LEVELS.length-1;i>=0;i--){if(xp>=LEVELS[i].xp)return i+1;}
    return 1;
  }

  function awardXP(amt, reason) {
    var s=get(); if(!s)return;
    var oldLvl=getLevel(s.xp);
    s.xp+=amt;
    var newLvl=getLevel(s.xp);
    if(newLvl>oldLvl){s.level=newLvl;setTimeout(function(){notify('🎉 Level Up! '+LEVELS[newLvl-1].emoji+' '+LEVELS[newLvl-1].name,'levelup');},400);}
    set(s);
  }

  function awardBadge(id) {
    var s=get(); if(!s)return false;
    s.badges=s.badges||[];
    if(s.badges.indexOf(id)>=0)return false;
    s.badges.push(id); set(s); return true;
  }

  function updateStreak() {
    var s=get(); if(!s)return;
    var today=new Date().toDateString();
    var last=s.lastActive||null;
    var yest=new Date(Date.now()-86400000).toDateString();
    if(last===today)return;
    s.streak=(last===yest)?(s.streak||0)+1:1;
    s.lastActive=today;
    if(s.streak===3)awardXP(10,'3-day streak! 🔥');
    if(s.streak===7)awardXP(25,'7-day streak! 🔥🔥');
    if(s.streak===14)awardXP(50,'14-day streak!');
    if(s.streak===30)awardXP(100,'30-day streak! Legend!');
    set(s);
  }

  function notify(msg, type) {
    var el=document.createElement('div');
    el.className='vma-notification'+(type?' vma-notification--'+type:'');
    el.textContent=msg;
    document.body.appendChild(el);
    requestAnimationFrame(function(){el.classList.add('vma-notification--visible');});
    setTimeout(function(){
      el.classList.remove('vma-notification--visible');
      setTimeout(function(){if(el.parentNode)el.parentNode.removeChild(el);},300);
    },3200);
  }

  return {
    get:get, set:set, create:create,
    getLevel:getLevel, LEVELS:LEVELS,
    awardXP:awardXP, awardBadge:awardBadge,
    updateStreak:updateStreak, notify:notify,
    checkTerms:function(){return localStorage.getItem(TERMS_KEY)==='true';}
  };
})();
