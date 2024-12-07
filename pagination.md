from flask import request

# Route: Course Management Page
@app.route('/admin/course_management', methods=['GET'])
def course_management():
    page = request.args.get('page', 1, type=int)  # Get the page number from the URL, default is 1
    per_page = 5  # Number of courses per page
    pagination = Course.query.paginate(page=page, per_page=per_page, error_out=False)
    courses = pagination.items
    return render_template(
        'admin/course_management.html', 
        courses=courses, 
        pagination=pagination
    )


{% extends 'admin/base.html' %} {% block content %}
<div class="container mx-auto">
  <!-- Page Title -->
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-bold">Course Management</h1>
    <button
      onclick="openModal('addCourseModal')"
      class="bg-blue-500 text-white py-2 px-6 rounded-lg hover:bg-blue-600 shadow-md"
    >
      + Add Course
    </button>
  </div>

  <!-- Table -->
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <thead
        class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
      >
        <tr>
          <th scope="col" class="px-6 py-3">Course Name</th>
          <th scope="col" class="px-6 py-3">Description</th>
          <th scope="col" class="px-6 py-3">Type</th>
          <th scope="col" class="px-6 py-3">Qualification</th>
          <th scope="col" class="px-6 py-3 text-right">Fee</th>
          <th scope="col" class="px-6 py-3 text-right">Duration</th>
          <th scope="col" class="px-6 py-3 text-right">
            <span class="sr-only">Actions</span>
          </th>
        </tr>
      </thead>
      <tbody>
        {% for course in courses %}
        <tr
          class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
        >
          <th
            scope="row"
            class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
          >
            {{ course.course_name }}
          </th>
          <td class="px-6 py-4 truncate max-w-xs">{{ course.description }}</td>
          <td class="px-6 py-4">{{ course.type }}</td>
          <td class="px-6 py-4">{{ course.qualification_type }}</td>
          <td class="px-6 py-4 text-right">₱{{ course.fee }}</td>
          <td class="px-6 py-4 text-right">{{ course.duration }} days</td>
          <td class="px-6 py-4 text-right">
            <button
              onclick="editCourse({{ course.id }})"
              class="text-blue-600 hover:underline font-medium text-xs"
            >
              Edit
            </button>
            <button
              onclick="deleteCourse({{ course.id }})"
              class="ml-2 text-red-600 hover:underline font-medium text-xs"
            >
              Delete
            </button>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <!-- Pagination Controls -->
  <div class="flex justify-between items-center mt-4">
    <div class="text-sm text-gray-700">
      Showing {{ pagination.page }} of {{ pagination.pages }} pages
    </div>
    <div class="flex space-x-2">
      {% if pagination.has_prev %}
      <a
        href="{{ url_for('course_management', page=pagination.prev_num) }}"
        class="bg-gray-300 text-gray-700 px-3 py-1 rounded-lg hover:bg-gray-400"
      >
        Previous
      </a>
      {% endif %}
      {% if pagination.has_next %}
      <a
        href="{{ url_for('course_management', page=pagination.next_num) }}"
        class="bg-gray-300 text-gray-700 px-3 py-1 rounded-lg hover:bg-gray-400"
      >
        Next
      </a>
      {% endif %}
    </div>
  </div>
</div>

{% include 'admin/add_course_modal.html' %}
{% include 'admin/update_course_modal.html' %}
<script src="/static/js/course.js"></script>
{% endblock %}
