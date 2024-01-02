; Fake_PNG.asm
; compile with
; nasm -f bin -o PNG.bin Fake_PNG.asm
section .data
  magic db 0x89, "PNG", 0x0d, 0x0a, 0x1a, 0x0a
  ihdr_length db 0, 0, 0, 13
  ihdr db "IHDR"