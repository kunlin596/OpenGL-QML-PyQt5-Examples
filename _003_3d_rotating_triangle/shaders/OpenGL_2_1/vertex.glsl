attribute highp vec3 position;
attribute highp vec3 color;
uniform highp mat4 model_matrix;
uniform highp mat4 view_matrix;
uniform highp mat4 projection_matrix;

varying vec3 pass_color;

void main () {
    mat4 m = projection_matrix * view_matrix * model_matrix;
    gl_Position = m * vec4(position, 1.0);
    pass_color = color;
}
