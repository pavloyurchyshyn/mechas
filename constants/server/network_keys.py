class PlayerAttrs:
    Token = 'token'
    Nickname = 'nickname'
    IsAdmin = 'is_admin'
    Ready = 'ready'
    Number = 'number'
    DefaultDetails = 'default_details'
    Position = 'position'


class NetworkKeys:
    Address = 'address'
    Port = 'port'
    Seed = 'seed'
    PlayerNumber = 'player_number'
    TeamNames = 'teams'
    AdminToken = 'admin_token'
    ServerMessages = 'server_message'
    ServerAnswer = 'server_answer'
    Password = 'password'

    DetailsPool = 'details_pool'
    DefaultDetails = 'default_details'
    DetailsPoolSettings = 'detail_pool_settings'
    DefaultDetailsSettings = 'default_details_settings'

    SwitchRoundStageTo = 'switch_round_stage'
    RoundStage = 'round_stage'
    RoundRoundStage = 'round'
    RoundLobbyStage = 'lobby'

    PlayersNumber = 'players_number'


class LobbyActions:
    Kick = 'kick'
    Start = 'start'


class ServerLobbyCategories:
    AddPlayer = 'add_player'
    KickPlayer = 'kick_player'
    StartGame = 'start_game'
    AddPlayersNumber = 'add_players_number'
    MinusPlayersNumber = 'minus_players_number'
    PlayersNumber = NetworkKeys.PlayersNumber


SLC = ServerLobbyCategories


class PlayerActions:
    DISCONNECT = 'disconnect'
    MESSAGE = 'message'
    READY_STATUS = 'ready_status'


class ServerConnectAnswers:
    CONNECTION_ANSWER = 'connection_answer'
    Connected = 'connected'
    WrongPassword = 'wrong_password'
    Banned = 'banned'
    ServerFull = 'server_full'
    FailedToConnect = 'failed'

    FAILED_ANSWERS = WrongPassword, Banned, ServerFull, FailedToConnect


class PlayerUpdates:
    Data = 'player_data'
    MechData = 'mech_data'
    Position = 'position'
    Energy = 'energy'

    UseCard = 'use_card'
    MechActions = 'mech_actions'
    ReadyStatus = 'ready_status'


class ServerResponseCategories:
    MatchTime = 'time'
    MessagesToAll = 'global_messages'

    PlayersUpdates = 'players_updates'
    CurrentPlayerActions = 'current_player_actions'
    DisconnectAll = 'disconnects_all'

    DeletePlayers = 'delete_players'

    ReadyState = 'ready_state'
    ReadyCount = 'ready_count'

    OtherPlayers = 'other_players'
    NewPlayers = 'new_players'


SRC = ServerResponseCategories


class ServerActions:
    DELETE_PLAYER = 'delete_player'
    DISCONNECT = 'disconnect'


class CheckRegex:
    # re to understand that is not few recv stacked
    good_recv_re = '^{"(' + PlayerActions.MESSAGE + ')|(' + ServerResponseCategories.MessagesToAll + ')":\s.*}{.*}$'
