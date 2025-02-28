// for (var index = 0; index < 5; index++) {
//     var btn = document.createElement('button');
//     btn.appendChild(document.createTextNode("Button " + index));
//     btn.addEventListener('click', function(){console.log(index);})
//     document.body.appendChild(btn);
    
// }

// Obj = {
//     "one": 1,
//     "two": 2,
//     "three": 3,
//     "four": 4,
//     "five": 5,
// }

let users =  [
    {user : "Sateesh", address : "Hyd", count : 10},
    {user : "Ranjith", address : "Delhi", count : 30},
    {user : "Rahul", address : "Mumbai", count : 110}
]

// function getUserCount(obj, user) {
//     let count;
//     obj.forEach(item => {
//         if(item.user === user) {
//             count = item.count
//         }
//     });
//     if (!count) {
//         return 'User not found'
//     }
//     else{
//         return count
//     }
// }
function getUserCount(obj, user) {
    let count;
    const filteredItem = obj.filter((item) => item.user == user);

    if (!filteredItem) {
        return 'User not found'
    }
    else{
        return filteredItem[0].count
    }
}

// getUserCount(users, "Sunny")
// console.log(getUserCount(users, "Sateesh"));

// for (var index = 1; index <= 2; index++) {
//     setTimeout(function(){console.log(index);}, 100);
    
// }

function f1() {
    if (true) {
        console.log(a);
        let a = 10;
        console.log(a);
    }
    console.log(a);
}

// f1();

let arr = [1, 2, 3, 4, 5, 6, 7, 8]
secondLastEle = arr.length-2
// console.log(arr[secondLastEle]);

// a = 3+ "3"
// console.log(typeof(a));
arr.push(7)
arr.unshift(1)

console.log(arr);