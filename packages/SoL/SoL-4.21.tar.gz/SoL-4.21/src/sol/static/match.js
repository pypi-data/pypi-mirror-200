// -*- coding: utf-8 -*-
// :Project:   SoL — Match digital scorecard
// :Created:   gio 22 dic 2022, 08:36:15
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2022, 2023 Lele Gaifax
//

//jsl:declare $

class MatchScorecard {
  constructor(max_allowed_boards, duration, pre_alarm, elapsed) {
    this.max_allowed_boards = max_allowed_boards;
    this.duration = duration;
    if(elapsed !== false && elapsed < 1000 * 60 * duration) {
      this.started_at = Date.now() - elapsed;
      this.pre_alarm_at = this.started_at + 1000 * 60 * (duration - pre_alarm);
    } else {
      this.started_at = false;
      this.pre_alarm_at = false;
    }
  }

  get boards_count() {
    return document.querySelectorAll('form > table > tbody > tr').length;
  }

  get countdown() {
    const started_at = this.started_at,
          pre_alarm_at = this.pre_alarm_at,
          now = Date.now(),
          progress = now - started_at,
          left = this.duration - (progress / 1000 / 60),
          mins = Math.trunc(left),
          secs = Math.trunc((left - mins) * 60);
    return { mins, secs, pre_alarm: pre_alarm_at && pre_alarm_at < now };
  }

  new_board_row(board) {
    // <tr id="board_${board}">
    //   <td class="center aligned" id="score_${board}_1"></td>
    //   <td class="center aligned">
    //     <div class="field">
    //       <input type="number" name="coins_${board}_1" min="0" max="9">
    //     </div>
    //   </td>
    //   <td class="collapsing">
    //     <div class="field">
    //       <div class="ui radio checkbox center aligned" id="cb_queen_${board}_1">
    //         <input type="radio" name="queen_${board}" value="1">
    //       </div>
    //     </div>
    //   </td>
    //   <td class="grey center aligned collapsing" colspan="2">${board}</td>
    //   <td class="collapsing">
    //     <div class="field">
    //       <div class="ui radio checkbox center aligned" id="cb_queen_${board}_2">
    //         <input type="radio" name="queen_${board}" value="2">
    //       </div>
    //     </div>
    //   </td>
    //   <td class="center aligned">
    //     <div class="field">
    //       <input type="number" name="coins_${board}_2" min="0" max="9">
    //     </div>
    //   </td>
    //   <td class="center aligned" id="score_${board}_2"></td>
    // </tr>;

    const tr = document.createElement('tr');
    tr.id = `board_${board}`;

    const score_c1 = document.createElement('td');
    score_c1.id = `score_${board}_1`;
    score_c1.className = 'center aligned';
    tr.appendChild(score_c1);

    const coins_c1 = document.createElement('td');
    coins_c1.className = 'center aligned';

    const coins_c1_field = document.createElement('div');
    coins_c1_field.className = 'field';

    const coins_c1_input = document.createElement('input');
    coins_c1_input.setAttribute('type', 'number');
    coins_c1_input.setAttribute('name', `coins_${board}_1`);
    coins_c1_input.setAttribute('min', '0');
    coins_c1_input.setAttribute('max', '9');
    coins_c1_field.appendChild(coins_c1_input);
    coins_c1.appendChild(coins_c1_field);
    tr.appendChild(coins_c1);

    const queen_c1 = document.createElement('td');
    queen_c1.className = 'collapsing';

    const queen_c1_field = document.createElement('div');
    queen_c1_field.className = 'field';

    const queen_c1_radio = document.createElement('div');
    queen_c1_radio.id = `cb_queen_${board}_1`;
    queen_c1_radio.className = 'ui radio checkbox center aligned';

    const queen_c1_input = document.createElement('input');
    queen_c1_input.setAttribute('type', 'radio');
    queen_c1_input.setAttribute('name', `queen_${board}`);
    queen_c1_input.setAttribute('value', '1');
    queen_c1_radio.appendChild(queen_c1_input);
    queen_c1_field.appendChild(queen_c1_radio);
    queen_c1.appendChild(queen_c1_field);
    tr.appendChild(queen_c1);

    const middle_col = document.createElement('td');
    middle_col.className = 'grey center aligned collapsing';
    middle_col.setAttribute('colspan', '2');
    middle_col.append(board);
    tr.appendChild(middle_col);

    const queen_c2 = document.createElement('td');
    queen_c2.className = 'collapsing';

    const queen_c2_field = document.createElement('div');
    queen_c2_field.className = 'field';

    const queen_c2_radio = document.createElement('div');
    queen_c2_radio.id = `cb_queen_${board}_2`;
    queen_c2_radio.className = 'ui radio checkbox center aligned';

    const queen_c2_input = document.createElement('input');
    queen_c2_input.setAttribute('type', 'radio');
    queen_c2_input.setAttribute('name', `queen_${board}`);
    queen_c2_input.setAttribute('value', '2');
    queen_c2_radio.appendChild(queen_c2_input);
    queen_c2_field.appendChild(queen_c2_radio);
    queen_c2.appendChild(queen_c2_field);
    tr.appendChild(queen_c2);

    const coins_c2 = document.createElement('td');
    coins_c2.className = 'center aligned';

    const coins_c2_field = document.createElement('div');
    coins_c2_field.className = 'field';

    const coins_c2_input = document.createElement('input');
    coins_c2_input.setAttribute('type', 'number');
    coins_c2_input.setAttribute('name', `coins_${board}_2`);
    coins_c2_input.setAttribute('min', '0');
    coins_c2_input.setAttribute('max', '9');
    coins_c2_field.appendChild(coins_c2_input);
    coins_c2.appendChild(coins_c2_field);
    tr.appendChild(coins_c2);

    const score_c2 = document.createElement('td');
    score_c2.id = `score_${board}_2`;
    score_c2.className = 'center aligned';
    tr.appendChild(score_c2);

    return tr;
  }

  add_board() {
    const self = this,
          new_board = self.boards_count + 1;

    for(var board = 1; board < new_board; board++) {
      const board_row = document.getElementById(`board_${board}`),
            queen_1_input = board_row.querySelector(`input[name="queen_${board}"][value="1"]`),
            queen_2_input = board_row.querySelector(`input[name="queen_${board}"][value="2"]`);

      queen_1_input.removeEventListener('change', self.show_reset_queen);
      queen_2_input.removeEventListener('change', self.show_reset_queen);
    }

    const row = self.new_board_row(new_board);
    document.getElementById('boards').appendChild(row);

    self.install_input_listeners(new_board);

    const table = document.querySelector('form table'),
          breaker = (table.classList.contains('breaker-1')
                     ? 1
                     : (table.classList.contains('breaker-2')
                        ? 2
                        : null)),
          ctors = table.querySelector('thead tr:first-child'),
          ctor1 = ctors.firstElementChild.querySelector('span'),
          ctor2 = ctors.lastElementChild.querySelector('span');
    var bctor, octor;

    if(new_board > 1)
      // After the first game hide the breaker radio
      document.querySelectorAll('div.breaker').forEach(div => {
        div.style.display = 'none';
      });

    if(breaker === 1) {
      bctor = ctor1;
      octor = ctor2;
    } else {
      bctor = ctor2;
      octor = ctor1;
    }
    if((new_board % 2) === 1) {
      bctor.classList.add('current-board-breaker');
      octor.classList.remove('current-board-breaker');
    } else {
      bctor.classList.remove('current-board-breaker');
      octor.classList.add('current-board-breaker');
    }

    document.getElementById('new_board_btn').classList.add('disabled');
  }

  install_input_listeners(board) {
    const self = this,
          board_row = document.getElementById(`board_${board}`),
          coins_1_input = board_row.querySelector(`input[name="coins_${board}_1"]`),
          coins_2_input = board_row.querySelector(`input[name="coins_${board}_2"]`),
          queen_1_input = board_row.querySelector(`input[name="queen_${board}"][value="1"]`),
          queen_2_input = board_row.querySelector(`input[name="queen_${board}"][value="2"]`),
          new_board_btn = document.getElementById('new_board_btn');

    function update_scores() {
      const score1 = parseInt(coins_1_input.value) || 0,
            score2 = parseInt(coins_2_input.value) || 0,
            done = score1 > 0 && score1 <= 9 || score2 > 0 && score2 <= 9;

      self.compute_scores_and_totals();
      if(done) {
        new_board_btn.focus();
        new_board_btn.scrollIntoView();
      }
    }

    coins_1_input.addEventListener('focus', event => coins_1_input.select());
    coins_2_input.addEventListener('focus', event => coins_2_input.select());
    coins_1_input.addEventListener('keyup', event => update_scores());
    coins_1_input.addEventListener('keydown', event => { coins_2_input.value = 0; });
    coins_2_input.addEventListener('keyup', event => update_scores());
    coins_2_input.addEventListener('keydown', event => { coins_1_input.value = 0; });
    queen_1_input.addEventListener('change', event => update_scores());
    queen_2_input.addEventListener('change', event => update_scores());

    if(board == self.boards_count && self.countdown.pre_alarm) {
      queen_1_input.addEventListener('change', self.show_reset_queen);
      queen_2_input.addEventListener('change', self.show_reset_queen);
    }
  }

  compute_scores_and_totals() {
    const boards = this.boards_count,
          new_board_btn = document.getElementById('new_board_btn'),
          end_match_btn = document.getElementById('end_match_btn');

    var total_1 = 0,
        total_2 = 0,
        last_ok = false;

    for(var board = 1; board <= boards; board++) {
      const board_row = document.getElementById(`board_${board}`),
            coins_1_input = board_row.querySelector(`input[name="coins_${board}_1"]`),
            coins_2_input = board_row.querySelector(`input[name="coins_${board}_2"]`),
            coins_1 = coins_1_input.value,
            coins_2 = coins_2_input.value,
            queen_1_input = board_row.querySelector(`input[name="queen_${board}"][value="1"]`),
            queen_2_input = board_row.querySelector(`input[name="queen_${board}"][value="2"]`),
            queen_1 = queen_1_input.checked,
            queen_2 = queen_2_input.checked;
      var score_1 = parseInt(coins_1) || 0,
          score_2 = parseInt(coins_2) || 0;

      if(score_1 > 9)
        coins_1_input.parentElement.classList.add('error');
      else
        coins_1_input.parentElement.classList.remove('error');

      if(score_2 > 9)
        coins_2_input.parentElement.classList.add('error');
      else
        coins_2_input.parentElement.classList.remove('error');

      if(score_1 > 9 || score_2 > 9) {
        new_board_btn.classList.add('disabled');
        end_match_btn.classList.add('disabled');
        return;
      } else {
        new_board_btn.classList.remove('disabled');
        end_match_btn.classList.remove('disabled');
      }
      // Did one of the player commit suicide? Check for an explicit '0' being entered
      if(coins_1 === '0' && coins_2 === '0') {
        if(queen_1)
          score_1 += total_1 < 22 ? 3 : 1;
        else if(queen_2)
          score_2 += total_2 < 22 ? 3 : 1;
      } else {
        if(queen_1 && score_1 > score_2 && total_1 < 22)
          score_1 += 3;
        else if(queen_2 && score_1 < score_2 && total_2 < 22)
          score_2 += 3;
      }

      const s1 = board_row.firstElementChild,
            s2 = board_row.lastElementChild;

      if(score_1 > score_2) {
        s1.classList.add('positive');
        s1.classList.remove('negative');
        s2.classList.add('negative');
        s2.classList.remove('positive');
      } else if(score_1 < score_2) {
        s1.classList.add('negative');
        s1.classList.remove('positive');
        s2.classList.add('positive');
        s2.classList.remove('negative');
      } else {
        s1.classList.add('positive');
        s1.classList.remove('negative');
        s2.classList.add('positive');
        s2.classList.remove('negative');
      }
      s1.innerText = score_1;
      s2.innerText = score_2;
      total_1 += score_1;
      total_2 += score_2;

      last_ok = coins_1 !== '' && coins_2 !== '' && (queen_1 || queen_2);
    }

    if(total_1 > 25) total_1 = 25;
    if(total_2 > 25) total_2 = 25;

    document.querySelector('input[name="score1"]').value = total_1;
    document.querySelector('input[name="score2"]').value = total_2;

    const t1 = document.getElementById('total_1'),
          t2 = document.getElementById('total_2');

    t1.innerHTML = `<big><strong>${total_1}</strong></big>`;
    t2.innerHTML = `<big><strong>${total_2}</strong></big>`;

    if(total_1 > total_2) {
      t1.classList.add('positive');
      t1.classList.remove('negative');
      t2.classList.add('negative');
      t2.classList.remove('positive');
    } else if(total_1 < total_2) {
      t1.classList.add('negative');
      t1.classList.remove('positive');
      t2.classList.add('positive');
      t2.classList.remove('negative');
    } else {
      t1.classList.add('positive');
      t1.classList.remove('negative');
      t2.classList.add('positive');
      t2.classList.remove('negative');
    }

    // Is last round complete?
    if(last_ok && boards < this.max_allowed_boards && total_1 < 25 && total_2 < 25)
      new_board_btn.classList.remove('disabled');
    else
      new_board_btn.classList.add('disabled');
  }

  show_countdown() {
    const self = this,
          countdown_div = document.getElementById('countdown'),
          stop_sign = document.getElementById('stop-sign'),
          end_match_btn = document.getElementById('end_match_btn');

    function update() {
      const {mins, secs, pre_alarm} = self.countdown;

      if(mins > 0 || secs > 0) {
        var remaining;

        if(mins > 0)
          remaining = `${mins}'`;
        if(secs > 0) {
          if(mins > 0)
            remaining += ` ${secs}"`;
          else
            remaining = `${secs}"`;
        }
        countdown_div.firstElementChild.innerText = remaining;
        if(pre_alarm) {
          const board = self.boards_count,
                board_row = document.getElementById(`board_${board}`),
                queen_1_input = board_row.querySelector(`input[name="queen_${board}"][value="1"]`),
                queen_2_input = board_row.querySelector(`input[name="queen_${board}"][value="2"]`);

          countdown_div.classList.add('pre-alarm');
          if(queen_1_input.checked || queen_2_input.checked)
            self.show_reset_queen();
          else {
            queen_1_input.addEventListener('change', self.show_reset_queen);
            queen_2_input.addEventListener('change', self.show_reset_queen);
          }
        }
      } else {
        countdown_div.firstElementChild.classList.add('invisible');
        countdown_div.classList.add('stop');
        stop_sign.classList.remove('invisible');
        end_match_btn.classList.add('blink');
        clearInterval(self.updateInterval);
        self.updateInterval = 0;
      }
    }

    countdown_div.classList.remove('invisible');
    self.updateInterval = setInterval(update, 1000 / 20);
  }

  show_reset_queen() {
    const reset_queen_row = document.querySelector('table tfoot tr:first-child');

    reset_queen_row.classList.remove('invisible');
  }

  init(newBoardLabel, confirmEndMessage) {
    const self = this,
          new_board_btn = document.getElementById('new_board_btn'),
          reset_queen_row = document.querySelector('table tfoot tr:first-child'),
          reset_queen_btn = reset_queen_row.querySelector('button');

    $('.checkbox').checkbox();
    if(self.played_boards > 0) {
      new_board_btn.innerText = newBoardLabel;
    }

    function reset_queen() {
      const board = self.boards_count,
            board_row = document.getElementById(`board_${board}`),
            queen_1_input = board_row.querySelector(`input[name="queen_${board}"][value="1"]`),
            queen_2_input = board_row.querySelector(`input[name="queen_${board}"][value="2"]`);

      queen_1_input.checked = false;
      queen_2_input.checked = false;
      reset_queen_row.classList.add('invisible');
      new_board_btn.classList.add('disabled');
    }

    reset_queen_btn.addEventListener('click', event => reset_queen());

    new_board_btn.addEventListener('click', event => {
      const board = self.boards_count;
      var should_add_new_board;

      if(board == 0)
        should_add_new_board = true;
      else if(board >= self.max_allowed_boards)
        should_add_new_board = false;
      else {
        const coins_1_input = document.querySelector(`input[name="coins_${board}_1"]`),
              coins_2_input = document.querySelector(`input[name="coins_${board}_2"]`),
              coins_1 = coins_1_input.value,
              coins_2 = coins_2_input.value,
              queen_1_input = document.getElementById(`cb_queen_${board}_1`).firstElementChild,
              queen_2_input = document.getElementById(`cb_queen_${board}_2`).firstElementChild,
              queen_1 = queen_1_input.checked,
              queen_2 = queen_2_input.checked,
              total_1 = document.getElementById('total_1').innerText,
              total_2 = document.getElementById('total_2').innerText;

        should_add_new_board = ((coins_1 || coins_2)
                                && parseInt(coins_1) < 10
                                && parseInt(coins_2) < 10
                                && (queen_1 || queen_2)
                                && parseInt(total_1) < 25
                                && parseInt(total_2) < 25);
      }

      if(should_add_new_board) {
        var $form = $('form.ui.form'),
            data = $form.serialize(),
            method = $form.attr('method'),
            url = document.URL;
        $.ajax({
          method: method,
          url: url,
          data: data
        }).done(function(result) {
          if(!result.success)
            alert(result.message);
          else if(result.elapsed && !self.started_at) {
            self.started_at = Date.now() - result.elapsed;
            self.show_countdown();
          }
        });
        self.add_board();
        new_board_btn.innerText = newBoardLabel;
        reset_queen_row.classList.add('invisible');
      }
    });

    $('thead .checkbox').change(function() {
      var breaker = null;

      if(document.querySelector('input[name="breaker"][value="1"]').checked)
        breaker = 1;
      else if(document.querySelector('input[name="breaker"][value="2"]').checked)
        breaker = 2;

      if(breaker) {
        const table = document.querySelector('form table'),
              other_breaker = breaker === 1 ? 2 : 1;
        table.classList.add(`breaker-${breaker}`);
        table.classList.remove(`breaker-${other_breaker}`);
      }

      if(self.boards_count === 0)
        new_board_btn.classList.remove('disabled');
    });

    /* This is needed to workaround a strange Firefox "feature": it seems to keep the state of
     * the radio when the user changes it and the refresh the page...
     * So we take the stored state, reflected in the breaker-X class on the table, and
     * initialize the radio accordingly. */
    const table = document.querySelector('form table'),
          breaker = (table.classList.contains('breaker-1')
                     ? 1
                     : (table.classList.contains('breaker-2')
                        ? 2
                        : null)),
          boards = self.boards_count;
    if(breaker) {
      const cboxes = $('thead .checkbox');
      if(breaker === 1) {
        cboxes.first().checkbox('set checked');
        cboxes.last().checkbox('set unchecked');
      } else {
        cboxes.first().checkbox('set unchecked');
        cboxes.last().checkbox('set checked');
      }
      if(boards > 1)
        // After the first game hide the breaker radio
        document.querySelectorAll('div.breaker').forEach(div => {
          div.style.display = 'none';
        });
    }

    for(var board=1; board <= boards; board++) {
      self.compute_scores_and_totals();
      self.install_input_listeners(board);
    }
    $("form").submit(function(event) {
      if(!confirm(confirmEndMessage))
        event.preventDefault();
    });

    if(self.started_at)
      self.show_countdown();
  }
}
