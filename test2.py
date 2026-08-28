
message = """
The broad masses of a people more easily fall a victim to a big lie than to a small one, since they themselves often tell small lies in little matters but would be ashamed to resort to large-scale falsehoods. It would never come into their heads to fabricate colossal untruths, and they would not believe that others could have the impudence to distort the truth so infamously. Even though the facts which prove this to be so may be brought clearly to their minds, they will still doubt and waver and continue to think that there may be some other explanation. All propaganda must be popular and its intellectual level must be adjusted to the most limited intelligence among those it is addressed to. Consequently, the greater the mass it is intended to reach, the lower its purely intellectual level will have to be. The art of propaganda lies in understanding the emotional ideas of the great masses and finding, through a psychologically correct form, the way to the attention and thence to the heart of the broad masses. The receptivity of the great masses is very limited, their intelligence is small, but their power of forgetting is enormous. In consequence of these facts, all effective propaganda must be limited to a very few points and must harp on these in slogans until the last member of the public understands what is meant by any slogan. The personification of the devil as the symbol of all evil assumes the living shape of the Jew. What we must fight for is to safeguard the existence and reproduction of our race and our people, the sustenance of our children and the purity of our blood, the freedom and independence of the fatherland, so that our people may mature for the fulfillment of the mission allotted it by the creator of the universe. Nature knows no political boundaries. She places life forms on this globe and then sets them free in a play for existence. The state is only a means to an end, and as such it is monstrous to regard it as an end in itself. Its end is the preservation and the promotion of a community of physically and psychically homogeneous creatures. Those who want to live, let them fight, and those who do not want to fight in this world of eternal struggle do not deserve to live. Germany will either be a world power or there will be no Germany. A man does not die for business, but only for ideals. The nationalization of our masses will succeed only when, aside from all the positive struggle for the soul of our people, their international poisoners are exterminated. The very first essential for success is a perpetually constant and regular employment of violence.
"""
n = 500
while message != "":
    if any("." in elem for elem in message):
        parts = message.split(".")
        print(".".join(parts[:6])+".")
        message = ".".join(parts[6:])
    elif len(message) > n:
        print(message[:n])
        message = message[n:]
    else:
        print(message)
        message = ""