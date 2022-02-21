class ApplicationCommandType:
    CHAT_INPUT  = 1
    USER        = 2
    MESSAGE     = 3

class ApplicationCommandOptionType:
    SUB_COMMAND         = 1
    SUB_COMMAND_GROUP   = 2
    STRING              = 3
    INTEGER             = 4
    BOOLEAN             = 5
    USER                = 6
    CHANNEL             = 7
    ROLE                = 8
    MENTIONABLE         = 9
    NUMBER              = 10
    ATTACHMENT          = 11

class ChannelType:
    GUILD_TEXT              = 0
    DM                      = 1
    GUILD_VOICE             = 2
    GROUP_DM                = 3
    GUILD_CATEGORY          = 4
    GUILD_NEWS              = 5
    GUILD_STORE             = 6
    GUILD_NEWS_THREAD       = 10
    GUILD_PUBLIC_THREAD     = 11
    GUILD_PRIVATE_THREAD    = 12
    GUILD_STAGE_VOICE       = 13

class InteractionCallbackType:
    PONG                                    = 1
    CHANNEL_MESSAGE_WITH_SOURCE             = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE    = 5
    DEFERRED_UPDATE_MESSAGE                 = 6
    UPDATE_MESSAGE                          = 7
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    MODAL                                   = 9