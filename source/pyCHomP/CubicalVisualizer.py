import IPython
import json
import random
import string
import os
import io
import subprocess
import pkgutil

def CubicalVisualizer(cells):

  def fix(value):
    if value == float("-Inf"): return 0
    if value == float("Inf"): return 5
    return value

  new_cells = [ [ [ fix(value) for value in I ] for I in cell.bounds() ] for cell in cells ]
  #print(new_cells)
  orbitcontrols = io.open('./js/OrbitControls.js','r',encoding='utf8').read()

  html_string = """
  <div id="marmalade_tuesday">
  </div>
  <script>
  requirejs(['files/js/three.js'], function (THREE) {
    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );

    var renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth/2.0, window.innerHeight/2.0 ); // made smaller
    document.getElementById("marmalade_tuesday").appendChild(renderer.domElement ); // placed where i wanted it

    """ + orbitcontrols + """
    controls = new THREE.OrbitControls( camera, renderer.domElement ); // to get control

    var data = """ + json.dumps(new_cells) + """;
    data.forEach(function(cell) {
      // midpoint (x,y,z) and widths (dx,dy,dz)
      var x = (cell[0][0] + cell[0][1])/2.0;
      var y = (cell[1][0] + cell[1][1])/2.0;
      var z = (cell[2][0] + cell[2][1])/2.0;
      var dx = cell[0][1]-cell[0][0];
      var dy = cell[1][1]-cell[1][0];
      var dz = cell[2][1]-cell[2][0];
      var dim = 3;
      if (dx > 0.0) dx = dx - .1;
      if (dx == 0.0 ){ dx = .1; dim = dim -1; }
      if (dy > 0.0 ) dy = dy - .1;
      if (dy == 0.0 ){ dy = .1; dim = dim -1; }
      if (dz > 0.0 ) dz = dz - .1;
      if (dz == 0.0 ){ dz = .1; dim = dim -1; }
      var cube_color = { 0 : 0x00ff00, 1 : 0xff0000, 2 : 0xff00ff, 3 : 0x0000ff };
      var geometry = new THREE.BoxGeometry( dx,dy,dz);
      var material = new THREE.MeshLambertMaterial( { color: cube_color[dim] } );
      var cube = new THREE.Mesh( geometry, material );
      cube.position.set(x,y,z); // to position it
      scene.add( cube );
    });

    // lights?
      var ambientLight = new THREE.AmbientLight( 0x000000 );
      scene.add( ambientLight );

      var lights = [];
      lights[ 0 ] = new THREE.PointLight( 0xffffff, 1, 0 );
      lights[ 1 ] = new THREE.PointLight( 0xffffff, 1, 0 );
      lights[ 2 ] = new THREE.PointLight( 0xffffff, 1, 0 );

      lights[ 0 ].position.set( 0, 200, 0 );
      lights[ 1 ].position.set( 100, 200, 100 );
      lights[ 2 ].position.set( - 100, - 200, - 100 );

      scene.add( lights[ 0 ] );
      scene.add( lights[ 1 ] );
      scene.add( lights[ 2 ] );
    // end lights

    // Camera position and look direction
    camera.position.x = 10.0;
    camera.position.y = 10.0;
    camera.position.z = 20.0;
    camera.lookAt(new THREE.Vector3(2.5,2.5,2.5))

    var render = function () {
      requestAnimationFrame( render );

      //cube.rotation.x += 0.1;
      //cube.rotation.y += 0.1;

      renderer.render(scene, camera);
      update();

    };
    function update()
    {
      // if ( keyboard.pressed("z") ) 
      // { 
      //   // do something
      // }
      
      controls.update();
      //stats.update();
    }
    render();

  });
  </script>
  """
  return IPython.display.HTML(html_string)
