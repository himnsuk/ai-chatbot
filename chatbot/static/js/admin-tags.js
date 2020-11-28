$(function () {
  var base_url = "http://localhost:5000"
  $('.included-tags-box').on('click', function (e) {
    if ($(e.target).hasClass('included-delete-button')) {
      var selectedTag = $(e.target).closest('.included-badge')
      $(e.target).removeClass('included-delete-button').addClass('excluded-delete-button').bind('click')
      var add_excluded_classes = selectedTag.removeClass('badge-primary included-badge').addClass('badge-danger excluded-tag ml-1')
      $('.excluded-tags-box').append(add_excluded_classes)
    }
  })

  $('.excluded-tags-box').on('click', function (e) {
    if ($(e.target).hasClass('excluded-delete-button')) {
      e.preventDefault()
      e.stopPropagation()
      var selectedTag = $(e.target).closest('.excluded-badge')
      selectedTag.remove()
    }
  })

  $('.tags-input').on('keyup', function (e) {
    var empty = false
    $('.tags-input').each(function () {
      if ($(this).val() == '') {
        empty = true
      }
    })

    if (empty) {
      $('.add-tags').attr('disabled', 'disabled')
    } else {
      $('.add-tags').removeAttr('disabled')
    }
  })

  $('.add-tags').on('click', function (e) {
    e.stopPropagation()
    var tags = $('.tags-input').val()
    if (tags !== "") {
      var tag_list = tags.trim().split(",")
      var tag_elements = ""
      tag_list.forEach(element => {
        if (element !== "") {
          tag_elements += `
                  <span class="badge badge-primary included-badge">
                  ${element} <i class="fa fa-times-circle ml-1 included-delete-button" aria-hidden="true"></i>
                  </span>
                  `
        }
      });
      $('.included-tags-box').append(tag_elements)
    }
    $('.tags-input').val('')
    $('.add-tags').attr('disabled', 'disabled')
  })

  $('.clear-tags').on('click', function () {
    $('.tags-input').val('')
    $('.add-tags').attr('disabled', 'disabled')
  })

  var selectedCourseModule = {}
  $('#pending-courses').on('change', function () {
    console.log("Selected item", $("#pending-courses").val())
    var selected_val = $("#pending-courses").val()
    var create_url = base_url + "/modules/" + selected_val;
    $.ajax({
      url: create_url,
      type: "GET",
      contentType: "application/json; charset=utf-8",
      success: function (data) {
        selectedCourseModule = data
        updateModuleDropdown(data)
      }
    })

    function updateModuleDropdown(data) {
      $('#pending-course-modules').find('option').remove()
      var modulesDropDown = '<option value="" disabled selected>Select Course Module</option>'
      data.forEach(element => {
        modulesDropDown += `<option value="${element.module_id}">${element.module_name}</option>`
      })

      $('#pending-course-modules').append(modulesDropDown)
    }
  })

  $('#pending-course-modules').on('change', function () {
    $('.included-tags-box').html('')
    var moduleId = $('#pending-course-modules').val()
    var getModule = selectedCourseModule.filter(item => item.module_id == moduleId)

    var included_tags = ''
    var excluded_tags = ''
    getModule[0].generated_tags.forEach(element => {
      included_tags += `<span class="badge badge-primary included-badge ml-1">
      ${element}<i class="fa fa-times-circle ml-1 included-delete-button" aria-hidden="true"></i>
    </span>`
    })

    getModule[0].excluded_tags.forEach(element => {
      excluded_tags += `<span class="badge badge-danger excluded-badge ml-1">
      ${element}<i class="fa fa-times-circle ml-1 excluded-delete-button" aria-hidden="true"></i>
    </span>`
    })

    $('.included-tags-box').append(included_tags)
    $('.excluded-tags-box').append(excluded_tags)
  })

  $('.submit-tags').on('click', function () {
    var included_tags = []
    var excluded_tags = []
    var included_items = $('.included-tags-box .included-badge')
    var excluded_items = $('.excluded-tags-box .excluded-badge')
    for (var i = 0; i < included_items.length; i++) {
      included_tags.push($(included_items[i]).text().trim())
    }

    for (var i = 0; i < excluded_items.length; i++) {
      excluded_tags.push($(excluded_items[i]).text().trim())
    }
    console.log("Included Tags List", included_tags)
    console.log("ExcludedTags List", excluded_tags)

    var create_url = base_url + "/update-module";
    var json_module = JSON.stringify({ 'module_id': selectedCourseModule[0].module_id, 'included_tags': included_tags.join(","), 'excluded_tags': excluded_tags.join(",")})

    $.ajax({
      url: create_url,
      type: "POST",
      data: json_module,
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function (data) {
        if(data.key == "Success"){
          location.reload()
        }
      }
    })
  })
})