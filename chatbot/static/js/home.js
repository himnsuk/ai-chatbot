$('document').ready(function () {
  var base_url = "http://localhost:5000"
  $("#student-list").change(function () {
    console.log("Event Triggered");
    var selected_val = $("#student-list").val();
    console.log(selected_val);
    var create_url = base_url + "/student-subscription/" + selected_val;
    console.log(create_url);
    $.ajax({
      url: create_url,
      type: "GET",
      contentType: "application/json; charset=utf-8",
      success: function (data) {
        console.log(data)
        addCourse(data)
      }
    })

    function addCourse(courseData) {
      var courseList = "";
      courseData.forEach(element => {
        courseList += `<li class="list-group-item">${element.course_name}</li>`
      });
      $(".list-group").empty();
      $(".list-group").append(courseList);
      $(".submit-link").empty();
      $(".submit-link").append(`<a href="${base_url + '/chatbot?student_id=' + selected_val}" class="btn btn-primary" role="button">Submit</a>`);
      // $(".submit-link").append(`<a href="${base_url + '/chatbot?student_id=' + selected_val}" class="btn btn-primary" role="button">Submit</a>`);
    }
  })
})