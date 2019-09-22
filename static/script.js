/**
 * Copyright 2018, Google LLC
 * Licensed under the Apache License, Version 2.0 (the `License`);
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an `AS IS` BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 
// [START gae_python37_log]
'use strict';

window.addEventListener('load', function () {

  //console.log("Hello World!");

});

function copy(text, target) {
  target = target.getElementsByTagName("span")[0];
  setTimeout(function() {
    var copied = document.getElementsByClassName("copied");
    for(var i = 0; i < copied.length; i++) {
      copied.item(i).innerHTML = copied.item(i).id;
      copied.item(i).classList.remove("copied")
    }
  }, 1000);
  target.classList.add("copied");
  target.innerHTML = "Copied!";
  var input = document.createElement('input');
  input.setAttribute('value', text);
  document.body.appendChild(input);
  input.select();
  var result = document.execCommand('copy');
  document.body.removeChild(input)
  return result;
}

function checkEnter(e) {
  if(e && e.keyCode == 13) {
    gooo();
  }
}

function gooo() {
  var inputVal = document.getElementById("input").value;
  location.href = "/query/" + inputVal;
}
// [END gae_python37_log]
