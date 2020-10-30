import os
import sys
from absl import app
from absl import flags
from typing import Any, List

from randomizer.logic.main import ZoraRandomizer
from randomizer.logic.rom import Rom
from randomizer.logic.settings import Settings

flags.DEFINE_integer(name='seed', default=0, help='The seed number to initialize RNG with.')
flags.DEFINE_string(name='flag_string',
                    default='',
                    help='The flags to use when randomizing the game')
flags.DEFINE_bool(name='debug_mode',
                  default=False,
                  help='Use debug mode with extra print statements and error checking')
flags.DEFINE_string(name='input_filename',
                    default='',
                    help='The filename of the vanilla ROM to randomize.')
flags.DEFINE_string(name='output_location',
                    default='',
                    help='The location to put the randomized ROM.')
COMMAND_LINE_FLAGS = flags.FLAGS


def main(unused_argv: Any) -> None:
  print("Seed is %s" % COMMAND_LINE_FLAGS.seed)
  print("Flag string is %s" % COMMAND_LINE_FLAGS.flag_string)
  settings = Settings(seed=COMMAND_LINE_FLAGS.seed,
                      flag_string=COMMAND_LINE_FLAGS.flag_string,
                      mode='standard',
                      debug_mode=COMMAND_LINE_FLAGS.debug_mode)
  randomizer = ZoraRandomizer(settings)
  randomizer.Randomize()
  patch = randomizer.GetPatch()

  (input_path, input_full_filename) = os.path.split(COMMAND_LINE_FLAGS.input_filename)
  (input_filename, input_extension) = os.path.splitext(input_full_filename)
  output_filename = os.path.join(
      COMMAND_LINE_FLAGS.output_location or input_path,
      "%s-randomized-%d%s" % (input_filename, COMMAND_LINE_FLAGS.seed, input_extension or ".nes"))
  output_rom = Rom(output_filename, src=COMMAND_LINE_FLAGS.input_filename)
  output_rom.OpenFile(write_mode=True)

  for address in patch.GetAddresses():
    data: List[int]
    data = patch.GetData(address)
    output_rom.WriteBytes(address, data)


if __name__ == '__main__':
  app.run(main)
