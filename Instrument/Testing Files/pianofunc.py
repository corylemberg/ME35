async def piano():

    # Note numbers for MIDI payloads
    note_number = {
        'C': 60, 'C#': 61, 'D': 62, 'D#': 63,
        'E': 64, 'F': 65, 'F#': 66, 'G': 67,
        'G#': 68, 'A': 69, 'A#': 70, 'B': 71
    }

    C = Pin('GPIO13', Pin.IN)
    Cs = Pin('GPIO12', Pin.IN)
    D = Pin('GPIO11', Pin.IN)
    Ds = Pin('GPIO10', Pin.IN)
    E = Pin('GPIO9', Pin.IN)
    F = Pin('GPIO8', Pin.IN)
    Fs = Pin('GPIO7', Pin.IN)
    G = Pin('GPIO6', Pin.IN)
    Gs = Pin('GPIO5', Pin.IN)
    A = Pin('GPIO4', Pin.IN)
    As = Pin('GPIO3', Pin.IN)
    B = Pin('GPIO2', Pin.IN)

    # Store previous values for toggling
    prevC = C.value()
    prevCs = Cs.value()
    prevD = D.value()
    prevDs = Ds.value()
    prevE = E.value()
    prevF = F.value()
    prevFs = Fs.value()
    prevG = G.value()
    prevGs = Gs.value()
    prevA = A.value()
    prevAs = As.value()
    prevB = B.value()

    while True:
        # Handle toggle for C
        if C.value() != prevC:
            if not C.value():
                print("C Toggle On")
                payload = bytes([tsM, tsL, cmd | channel, note_number['C'], velocity['f']])
                p.send(payload)
            else:
                print("C Toggle OFF")
                payload = bytes([tsM, tsL, cmd | channel, note_number['C'], velocity['off']])
                p.send(payload)
            prevC = C.value()

        # Handle toggle for Cs
        if Cs.value() != prevCs:
            if not Cs.value():
                print("Cs Toggle On")
                payload = bytes([tsM, tsL, cmd | channel, note_number['C#'], velocity['f']])
                p.send(payload)
            else:
                print("Cs Toggle OFF")
                payload = bytes([tsM, tsL, cmd | channel, note_number['C#'], velocity['off']])
                p.send(payload)
            prevCs = Cs.value()

        # Handle toggle for D
        if D.value() != prevD:
            if not D.value():
                print("D Toggle On")
                payload = bytes([tsM, tsL, cmd | channel, note_number['D'], velocity['f']])
                p.send(payload)
            else:
                print("D Toggle OFF")
                payload = bytes([tsM, tsL, cmd | channel, note_number['D'], velocity['off']])
                p.send(payload)
            prevD = D.value()

        # Handle toggle for Ds
        if Ds.value() != prevDs:
            if not Ds.value():
                print("Ds Toggle On")
                payload = bytes([tsM, tsL, cmd | channel, note_number['D#'], velocity['f']])
                p.send(payload)
            else:
                print("Ds Toggle OFF")
                payload = bytes([tsM, tsL, cmd | channel, note_number['D#'], velocity['off']])
                p.send(payload)
            prevDs = Ds.value()

        # Handle toggle for E
        if E.value() != prevE:
            if not E.value():
                print("E Toggle On")
                payload = bytes([tsM, tsL, cmd | channel, note_number['E'], velocity['f']])
                p.send(payload)
            else:
                print("E Toggle OFF")
                payload = bytes([tsM, tsL, cmd | channel, note_number['E'], velocity['off']])
                p.send(payload)
            prevE = E.value()

        # Handle toggle for F
        if F.value() != prevF:
            if not F.value():
                print("F Toggle On")
                payload = bytes([tsM, tsL, cmd | channel, note_number['F'], velocity['f']])
                p.send(payload)
            else:
                print("F Toggle OFF")
                payload = bytes([tsM, tsL, cmd | channel, note_number['F'], velocity['off']])
                p.send(payload)
            prevF = F.value()

        # Handle toggle for Fs
        if Fs.value() != prevFs:
            if not Fs.value():
                print("Fs Toggle On")
                payload = bytes([tsM, tsL, cmd | channel, note_number['F#'], velocity['f']])
                p.send(payload)
            else:
                print("Fs Toggle OFF")
                payload = bytes([tsM, tsL, cmd | channel, note_number['F#'], velocity['off']])
                p.send(payload)
            prevFs = Fs.value()

        # Handle toggle for G
        if G.value() != prevG:
            if not G.value():
                print("G Toggle On")
                payload = bytes([tsM, tsL, cmd | channel, note_number['G'], velocity['f']])
                p.send(payload)
            else:
                print("G Toggle OFF")
                payload = bytes([tsM, tsL, cmd | channel, note_number['G'], velocity['off']])
                p.send(payload)
            prevG = G.value()

        # Handle toggle for Gs
        if Gs.value() != prevGs:
            if not Gs.value():
                print("Gs Toggle On")
                payload = bytes([tsM, tsL, cmd | channel, note_number['G#'], velocity['f']])
                p.send(payload)
            else:
                print("Gs Toggle OFF")
                payload = bytes([tsM, tsL, cmd | channel, note_number['G#'], velocity['off']])
                p.send(payload)
            prevGs = Gs.value()

        # Handle toggle for A
        if A.value() != prevA:
            if not A.value():
                print("A Toggle On")
                payload = bytes([tsM, tsL, cmd | channel, note_number['A'], velocity['f']])
                p.send(payload)
            else:
                print("A Toggle OFF")
                payload = bytes([tsM, tsL, cmd | channel, note_number['A'], velocity['off']])
                p.send(payload)
            prevA = A.value()

        # Handle toggle for As
        if As.value() != prevAs:
            if not As.value():
                print("As Toggle On")
                payload = bytes([tsM, tsL, cmd | channel, note_number['A#'], velocity['f']])
                p.send(payload)
            else:
                print("As Toggle OFF")
                payload = bytes([tsM, tsL, cmd | channel, note_number['A#'], velocity['off']])
                p.send(payload)
            prevAs = As.value()

        # Handle toggle for B
        if B.value() != prevB:
            if not B.value():
                print("B Toggle On")
                payload = bytes([tsM, tsL, cmd | channel, note_number['B'], velocity['f']])
                p.send(payload)
            else:
                print("B Toggle OFF")
                payload = bytes([tsM, tsL, cmd | channel, note_number['B'], velocity['off']])
                p.send(payload)
            prevB = B.value()

        await asyncio.sleep(0.01)