attribute highp vec3 position;
attribute highp vec3 color;

varying vec3 pass_color;

void main () {
    gl_Position = vec4(position, 1.0);
    pass_color = color;
}
