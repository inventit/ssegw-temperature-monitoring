{ 'includes': [
    'common.gypi',
    'config.gypi',
  ],
  'targets': [
    # your M2M/IoT application
    {
      'target_name': '<(package_name)',
      'sources': [
        'src/uploader.c',
        'src/switch.c',
        'src/sensor.c',
        'src/led.c',
        'src/<(package_name).c',
       ],
      'product_prefix': '',
      'type': 'shared_library',
      'cflags': [ '-fPIC' ],
      'include_dirs' : [
      ],
      'libraries': [
        '-lmoatapp',
      ],
      'dependencies': [
      ],
      'conditions': [
        ['target_product == "Armadillo-IoT"', {
          'cflags': [ '-DPRODUCT_AG4XX' ],
        }],
        ['target_product == "RaspberryPi"', {
          'cflags': [ '-DPRODUCT_RASPI' ],
        }],
        ['target_product == "OpenBlocks-IoT"', {
          'cflags': [ '-DPRODUCT_OBSIOT' ],
        }],
      ],
    },
  ],
}
