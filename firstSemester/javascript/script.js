console.log ('Dunnie');
>
//age -> string
//let ageString = age.toString(16);
let ageString = String(age);
console.log ( ageString );
//age -> number
let ageNum = Number(ageString);
 console.log (ageNum);
let ageInt = parseInt(ageString);
let ageFloat = parseFloat(age);
console.log (ageFloat, ageInt);
/**
 * this is a multi line comment
 */

//Boolean -> any other data types
let isTutor = false;
console.log(typeof isTutor);
//Number
let isTutorNum = Number(isTutor);
console.log(isTutorNum);

// falsy values -> false, 0, '', null, undefined, NaN
// truthy values -> true, any number except 0, any string except empty string, {}, [], function

let 2pac ="4real@gmail.com";