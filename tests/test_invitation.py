from vitality.invitation import Invitation


def test_invitation_creation():

    invitation = Invitation("123456789012345678901234",
                            "432109876543210987654321",
                            "718293712893718927389127")

    assert invitation._id == "123456789012345678901234"
    assert invitation.sender == "432109876543210987654321"
    assert invitation.recipient == "718293712893718927389127"


def test_invitation_repr():

    invitation = Invitation("123456789012345678901234",
                            "432109876543210987654321",
                            "718293712893718927389127")

    assert repr(invitation) \
        == 'Invitation(123456789012345678901234, 432109876543210987654321, 718293712893718927389127)'
